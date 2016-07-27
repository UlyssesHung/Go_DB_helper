import json
import time
import datetime
import resource


class fixinfo:
    servicestartdt = datetime.date(2013, 1, 1)
    yesterday = datetime.datetime.now().date() + datetime.timedelta(days=-1)
    today = datetime.datetime.now()
    todaydt = today.date()
    todaydtint = time.mktime(todaydt.timetuple())


class JsonItemClass(json.JSONEncoder):

    def tojson(self):
        return json.dumps(self, default=self.default, sort_keys=True, indent=4,
                          ensure_ascii=False)

    def toutf8json(self):
        return json.dumps(self, default=self.default, sort_keys=True, indent=4,
                          ensure_ascii=False, encoding='utf8')

    # special purpose function does not includes into unitest
    # We need inherited json.JSONENcoder to make json.loads works.
    # However, when we inherited, the json.dumps in tojson() will includes
    # attribute from parent. It is not what we want.
    def default(self, o=None):
        d = None
        if o is None:
            d = self.__dict__
        else:
            d = o.__dict__
        if hasattr(o, "rsvdt"):
            if isinstance(o.rsvdt, datetime.date):
                d["rsvdt"] = dict(year=o.rsvdt.year,
                                  month=o.rsvdt.month, day=o.rsvdt.day)
            else:
                d["rsvdt"] = o.rsvdt.__dict__
        if hasattr(o, "crtdt"):
            if isinstance(o.crtdt, datetime.date):
                d["crtdt"] = dict(year=o.crtdt.year,
                                  month=o.crtdt.month, day=o.crtdt.day)
            else:
                d["crtdt"] = o.crtdt.__dict__
        if hasattr(o, "lastrsvdt"):
            if isinstance(o.lastrsvdt, datetime.date):
                d["lastrsvdt"] = dict(year=o.lastrsvdt.year,
                                      month=o.lastrsvdt.month,
                                      day=o.lastrsvdt.day)
            else:
                d["lastrsvdt"] = o.lastrsvdt.__dict__

        if hasattr(o, "lastcrtdt"):
            if isinstance(o.lastcrtdt, datetime.date):
                d["lastcrtdt"] = dict(year=o.lastcrtdt.year,
                                      month=o.lastcrtdt.month,
                                      day=o.lastcrtdt.day)
            else:
                d["lastcrtdt"] = o.lastcrtdt.__dict__

        if "allow_nan" in d:
            del d["allow_nan"]
        if "check_circular" in d:
            del d["check_circular"]
        if "encoding" in d:
            del d["encoding"]
        if "ensure_ascii" in d:
            del d["ensure_ascii"]
        if "indent" in d:
            del d["indent"]
        if "skipkeys" in d:
            del d["skipkeys"]
        if "sort_keys" in d:
            del d["sort_keys"]
        return d


def memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1204)


def round_float_list(li, n=2):
    newFlist = []
    for f in li:
        if type(f) == int:
            newFlist.append(f)
        else:
            newFlist.append(round(f, n))
    return newFlist


def try_parse_int(value):
    try:
        return int(value), True
    except ValueError:
        return value, False
