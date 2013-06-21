from sunlight import openstates
from flask import Flask, render_template

from collections import Counter
from scipy.stats import zscore

import json


app = Flask(__name__)
blacklist = []


def do_math(what):
    what = sorted([(x, y) for x, y in what.items()], key=lambda x: x[1])
    what.reverse()
    values = list(map(lambda x: x[1], what))
    x = zip(zscore(values), what)
    return x


@app.route("/view/<who>")
def view(who):
    return render_template('view.html', who=who)

@app.route("/data/<who>")
def data(who):
    sponsored_bills = openstates.bills(sponsor_id=who, fields='subjects')
    count = Counter([el for sl in map(lambda x: x.get('subjects', []),
                                      sponsored_bills) for el in sl])
    [count.pop(x) for x in blacklist if x in count]
    ret = do_math(count)

    additive = min(map(lambda x: x[0], ret))
    if additive >= 0:
        additive = 0
    else:
        additive = (-additive) + 1

    output = []
    for el in ret:
        output.append([
            el[0] + additive,
            el[1]
        ])

    return json.dumps(output)


if __name__ == '__main__':
    app.run(debug=True)

