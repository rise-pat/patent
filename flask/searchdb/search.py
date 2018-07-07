from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from searchdb.db import get_db
from flask import jsonify
import json
from searchdb.search_utils import utility

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=(['GET']))
def init():
    return render_template('search/search_json.html')

@bp.route('/json_query', methods=(['POST']))
def getjson():

    json_data = request.get_json()
    query = json_data['vue_query']
    drilldown = json_data['drilldown']
    error = None

    if not query :
        error = 'Query is required'
    if error is not None:
        flash(error)
    else:
        db = get_db()
        cursor = db.cursor()

        sql = "select mroonga_command(\'select --table publn_data "
        sql += "--match_columns \\\'title * 100 || claims * 100 || description\\\' --query \"" + query + "\" "

        output_columns = "id,type,appln_nr,publn_nr,reg_nr,filing_date,pub_date,reg_date,title,applicants,attorneys,inventors,fi,clsf"
        #出願人指定の場合
        if 'drilldown_query_type' in request.form:
            drilldown_query_type = request.form['drilldown_query_type']
            drilldown_query = request.form['drilldown_query']
            if drilldown_query_type and drilldown_query:
                sql += "--filter \\\'" + drilldown_query_type +" @ \\\"" + drilldown_query + "\\\"\\\' "

        if drilldown != "none":
            sql += "--drilldown " + drilldown + " --drilldown_sort_keys \\\'-_nsubrecs,-_score\\\' --limit 0 --drilldown_limit 100 "
        else:
            sql += "--output_columns " + output_columns + " --limit 50 "

        sql += "\')  AS MROONGA_COMMAND"

        cursor.execute(sql)

        results = cursor.fetchall()
        cursor.close()
        #print(results)
        value  = list(results[0].values())
        json_str = str(value[0], encoding='utf-8', errors='replace')
        result_json =  (json.loads(json_str))[0]
        results = []
        count = result_json[0][0]

        converted_json_obj = utility.convertResultJSON(json_str)

        return jsonify(converted_json_obj)
