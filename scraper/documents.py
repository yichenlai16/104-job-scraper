from elasticsearch_dsl import Document, Text, Integer, Date, Keyword


class JobItemDocument(Document):
    jobName = Text()
    jobRole = Integer()
    jobAddrNoDesc = Text()
    jobAddress = Text()
    description = Text()
    optionEdu = Text()
    periodDesc = Text()
    applyCnt = Integer()
    custName = Text()
    coIndustryDesc = Text()
    salaryLow = Integer()
    salaryHigh = Integer()
    appearDate = Date()
    jobLink = Keyword()
    remoteWorkType = Integer()
    major = Text(multi=True)
    salaryType = Text()

    class Index:
        name = os.getenv("ELASTICSEARCH_INDEX")
