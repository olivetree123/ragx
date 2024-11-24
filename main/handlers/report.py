from copy import copy

from main import (
    models,
    params,
    results,
)
from main.response import (
    OkResponse,
    FailResponse,
    APIStatus,
)
from main.md.current import current_project


def GetReportHandler(request, report_id: str):
    try:
        report = models.Report.objects.get(id=report_id,
                                           project_id=current_project())
    except models.Report.DoesNotExist:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND, message="报告不存在")
    return OkResponse(results.ReportResult.from_orm(report))


def CreateReportHandler(request, param: params.CreateReportParam):
    instances_to_create = []
    instances_to_update = []
    for item in param.reports:
        instance = models.Report.get_by_query(query=item.query,
                                              methods=[item.method],
                                              paragraph_id=item.paragraph_id,
                                              project_id=item.project_id)
        if instance is None:
            instances_to_create.append(models.Report(**item.dict()))
        else:
            instance.paragraph_title = item.paragraph_title
            instance.paragraph_content = item.paragraph_content
            instances_to_update.append(instance)
    if instances_to_create:
        models.Report.objects.bulk_create(instances_to_create)
    if instances_to_update:
        models.Report.objects.bulk_update(
            instances_to_update, ["paragraph_title", "paragraph_content"])
    return OkResponse()


def UpdateReportHandler(request, report_id: str,
                        param: params.UpdateReportParam):
    try:
        report = models.Report.objects.get(id=report_id)
    except models.Report.DoesNotExist:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    report.update(**param.dict())
    return results.ReportResult.from_orm(report)


def DeleteReportHandler(request, report_id: str):
    models.Report.objects.filter(id=report_id).delete()
    return OkResponse()


def MarkReportHandler(request, param: params.MarkReportParam):
    """给报告打分"""
    report = models.Report.get_by_query(query=param.query,
                                        methods=param.methods,
                                        paragraph_id=param.paragraph_id,
                                        project_id=current_project())
    if not report:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    report.score = param.score
    report.save()
    return OkResponse(results.ReportResult.from_orm(report))


# class ResultItem(object):
#     def __init__(self, query, method, paragraph_id):
#         self.query = query
#         self.method = method
#         self.paragraph_id = paragraph_id

# class ResultEntity(object):
#     def __init__(self, query):
#         self.query = query
#         self.intersection = []
#         self.items = []

#     def add_item(self, item: ResultItem):
#         current_item = None
#         for item in self.items:
#             if item.method == item.method:
#                 current_item = item
#                 break
#         if current_item is None:
#             current_item =

#         current_item


def ListReportMethodsHandler(request):
    # distinct 操作可以利用索引来提高查询性能
    # 如果你使用的是 PostgreSQL 数据库，可以使用 distinct 和 order_by 结合的方式来进一步优化查询性能
    rs = models.Report.objects.order_by("method").values("method").distinct()
    rs = [r["method"] for r in rs]
    return OkResponse(rs)


def ListReportHandler(request, param: params.ListReportParam):
    # begin = (param.page - 1) * param.page_size
    reports = models.Report.objects.all()
    if param.methods:
        reports = reports.filter(method__in=param.methods)
    # reports = reports[begin:begin + param.page_size]
    result = {}
    for report in reports:
        query = report.query
        if query not in result:
            result[query] = {
                "query": report.query,
                "items": [],
                "project_id": report.project_id,
            }
        current_item = None
        items = result[query]["items"]
        for item in items:
            if item["method"] == report.method:
                current_item = item
                break
        if current_item is None:
            current_item = {
                "method": report.method,
                "paragraphs": [],
                "positive": 0,
                "negative": 0
            }
            items.append(current_item)

        current_item["paragraphs"].append({
            "id": report.paragraph_id,
            "title": report.paragraph_title,
            "score": report.score,
        })

    # 计算交集
    for _, value in result.items():
        intersection = []
        intersection_ids = set()
        items = value["items"]
        if len(items) > 1:
            intersection_ids = set([p["id"] for p in items[0]["paragraphs"]])
            for item in items[1:]:
                intersection_ids = intersection_ids & set(
                    [p["id"] for p in item["paragraphs"]])
            # value["intersection"] = list(intersection)

        for i, item in enumerate(items):
            paragraphs = item["paragraphs"]
            for j in range(len(paragraphs)):
                if paragraphs[j]["id"] in intersection_ids:
                    if i == 0:
                        intersection.append(copy(paragraphs[j]))
                    paragraphs[j] = None
            items[i]["paragraphs"] = [p for p in paragraphs if p is not None]

        value["intersection"] = intersection
        value["intersection_ids"] = list(intersection_ids)
        value["items"] = sorted(items, key=lambda x: x["method"])
    return OkResponse(list(result.values()))
