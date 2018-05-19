import hashlib


class LagouJobInfo(object):
    def __init__(self, title, address, salary, workYear, company, financeStage):
        if address is None:
            address = '不详'
        self.title = title
        self.address = address
        self.salary = salary
        self.workYear = workYear
        self.company = company
        self.financeStage = financeStage

    def get_MD5(self):
        m = hashlib.md5()
        m.update(str(self.__dict__).encode('utf-8'))
        return m.hexdigest()
