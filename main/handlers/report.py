from main import (
    models,
    params,
    results,
)
from main.response import BadRequestError


def GetReportHandler(request, report_id: str):
    try:
        report = models.Report.objects.get(id=report_id)
    except models.Report.DoesNotExist:
        raise BadRequestError(message="Report not found")
    return results.ReportResult.from_orm(report)


def CreateReportHandler(request, param: params.CreateReportParam):
    instances_to_create = []
    instances_to_update = []
    for item in param.reports:
        instance = models.Report.get_by_query(query=item.query,
                                              method=item.method,
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
    return {}


def UpdateReportHandler(request, report_id: str,
                        param: params.UpdateReportParam):
    try:
        report = models.Report.objects.get(id=report_id)
    except models.Report.DoesNotExist:
        return BadRequestError(message="Report not found")
    report.update(**param.dict())
    return results.ReportResult.from_orm(report)


def DeleteReportHandler(request, report_id: str):
    print(f"pretend to delete report where report_id={report_id}")
    return {}


def SetReportStatusHandler(request, report_id: str, status: int):
    try:
        report = models.Report.objects.get(id=report_id)
    except models.Report.DoesNotExist:
        return BadRequestError(message="Report not found")
    report.match_status = status
    report.save()
    return results.ReportResult.from_orm(report)


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


def ListReportHandler(request):
    reports = models.Report.objects.all()
    result = {}
    for report in reports:
        query = report.query
        if query not in result:
            result[query] = {
                "query": report.query,
                "intersection": [],
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
            "status": 0,
        })
    return list(result.values())
