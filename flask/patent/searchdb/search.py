from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from searchdb.db import get_db
import json

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=('GET','POST'))
def search():
    if request.method == 'POST':
        query = request.form['query']
        drilldown = request.form['drilldown']
        error = None

        if not query :
            error = 'Query is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()

            sql = "select mroonga_command(\'select --table publn_data "
            sql += "--match_columns \\\'title * 7 || claims * 5 || description\\\' --query \"" + query + "\" "

            #出願人指定の場合
            if 'drilldown_query_type' in request.form:
                drilldown_query_type = request.form['drilldown_query_type']
                drilldown_query = request.form['drilldown_query']
                if drilldown_query_type and drilldown_query:
                    sql += "--filter \\\'" + drilldown_query_type +" @ \\\"" + drilldown_query + "\\\"\\\' "

            if drilldown != "none":
                sql += "--drilldown " + drilldown + " --drilldown_sort_keys \\\'-_nsubrecs,-_score\\\' --limit 0 --drilldown_limit 100 "
            else:
                sql += "--output_columns publn_nr,title,applicants --limit -1 "

            sql += "\')  AS MROONGA_COMMAND"
            print(sql)
            cursor.execute(sql)

            results = cursor.fetchall()
            cursor.close()
            #print(results)
            value  = list(results[0].values())
            json_str = str(value[0], encoding='utf-8', errors='replace')
            result_json =  (json.loads(json_str))[0]
            results = []
            count = result_json[0][0]

            if drilldown == "none":
                result_json = (json.loads(json_str))[0]
                for idx in range(2, len(result_json)):
                    temp = {}
                    for i in range(len(result_json[idx])):
                        if isinstance(result_json[idx][i], list):
                            temp[result_json[1][i][0]] = '、'.join(result_json[idx][i])
                        else:
                            temp[result_json[1][i][0]] = result_json[idx][i]
                    results.append(temp)
            else:
                result_json = (json.loads(json_str))[1]

                for idx in range(3, len(result_json)):
                    temp = {}
                    for i in range(len(result_json[idx])):
                        if isinstance(result_json[idx][i], list):
                            temp[result_json[1][i][0]] = '、'.join(result_json[idx][i])
                        else:
                            temp[result_json[1][i][0]] = result_json[idx][i]
                    results.append(temp)

            return render_template('search/search.html', count=count, results=results,query=query, drilldown = drilldown)

    return render_template('search/search.html')
