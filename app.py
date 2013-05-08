from sunlight import openstates
from flask import Flask, render_template

from collections import Counter
from scipy.stats import zscore


app = Flask(__name__)
blacklist = []


def do_math(what):
    what = sorted([(x, y) for x, y in what.items()], key=lambda x: x[1])
    values = map(lambda x: x[1], what)
    ret = sorted(zip(zscore(values), what), key=lambda x: x[0])
    ret.reverse()
    return ret


@app.route("/view/<who>")
def index(who):
    sponsored_bills = openstates.bills(sponsor_id=who, fields='subjects')
    count = Counter([el for sl in map(lambda x: x.get('subjects', []),
                                      sponsored_bills) for el in sl])
    [count.pop(x) for x in blacklist if x in count]
    return render_template('view.html', values=do_math(count))


if __name__ == '__main__':
    app.run(debug=True)

