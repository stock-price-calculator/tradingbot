import datetime


def cal_day_data(term):
    thelatest_date = []
    current_date = datetime.date.today()

    for i in range(0, term):
        s = current_date - datetime.timedelta(days=i)
        print(s)
        splits = str(s).split("-")
        aggre_s = splits[0] + splits[1] + splits[2]
        print("hong : "+ aggre_s)
        sweek = datetime.date(int(splits[0]), int(splits[1]), int(splits[2])).weekday()
        print(sweek)
        if sweek > 4:
            pass
        else:
            thelatest_date.append(aggre_s)

    return thelatest_date

cal_day_data(10)


