class Report:
    def generate(self):
        print("Report generated")


class Dashboard:
    def __init__(self, report):
        self.report = report

    def show(self):
        self.report.generate()


report = Report()
dashboard = Dashboard(report)

dashboard.show()
