from flask import jsonify, request, abort
import sqlalchemy
from sqlalchemy.sql import text
from flask_cors import cross_origin
from config import app, con
from datetime import datetime

# Get all records in datatable


@app.route('/datatable/all', methods=['GET'])
@cross_origin()
def get_all_data():
    select_query = text('SELECT * FROM osf_public.datatable')
    rs = con.execute(select_query)
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        duration_days = datetime.now() - tempDict['added_date']
        if tempDict['closed_date']:
            duration_days = tempDict['closed_date'] - tempDict['added_date']
        tempDict['duration_days'] = duration_days.days
        duration_edits = datetime.now() - tempDict['last_edit']
        tempDict['duration_edits'] = duration_edits.days
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200


@app.route('/datatable/open', methods=['GET'])
@cross_origin()
def get_open_data():
    select_query = text(
        "SELECT * FROM osf_public.datatable WHERE status = 'OPEN'")
    rs = con.execute(select_query)
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        duration_days = datetime.now() - tempDict['added_date']
        if tempDict['closed_date']:
            duration_days = tempDict['closed_date'] - tempDict['added_date']
        tempDict['duration_days'] = duration_days.days
        duration_edits = datetime.now() - tempDict['last_edit']
        tempDict['duration_edits'] = duration_edits.days
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200


@app.route('/datatable/owner/<string:owner>', methods=['GET'])
@cross_origin()
def get_owner_data(owner):
    select_query = text(
        'SELECT * FROM osf_public.datatable WHERE owner = :owner')
    rs = con.execute(select_query, {'owner': owner})
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        duration_days = datetime.now() - tempDict['added_date']
        if tempDict['closed_date']:
            duration_days = tempDict['closed_date'] - tempDict['added_date']
        tempDict['duration_days'] = duration_days.days
        duration_edits = datetime.now() - tempDict['last_edit']
        tempDict['duration_edits'] = duration_edits.days
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200


@app.route('/datatable/owners', methods=['GET'])
def get_owners():
    select_query = text('SELECT DISTINCT owner FROM datatable')
    rs = con.execute(select_query)
    rows = rs.fetchall()
    owners = [row[0] for row in rows]
    return jsonify(owners), 200


@app.route('/datatable', methods=['POST'])
@cross_origin()
def create_data():
    data = request.get_json(force=True)
    insert_query = text("INSERT INTO datatable (business_unit, ship, tve, part_number, description, assembly, qty, code, owner, need_date, ecd, previous_ecd, impact, comment, status, last_edit, added_date, on_board, closed_date, manager, ntid) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL, '%s', '%s') RETURNING id;" % (
        data['business_unit'], data['ship'], data['tve'], data['part_number'], data['description'], data['assembly'], data['qty'], data['code'], data['owner'], data['need_date'], data['ecd'], data['previous_ecd'], data['impact'], data['comment'], data['status'], data['last_edit'], data['added_date'], data['on_board'], data['manager'], data['ntid']))
    result = con.execute(insert_query)
    new_id = result.fetchone()[0]

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 201 Created
    return jsonify({"Data was successfully created. id": new_id}), 201

# Update a template and its nodes


@app.route('/datatable/<int:_id>', methods=['PUT'])
@cross_origin()
def update_data(_id):
    data = request.get_json(force=True)
    update_query = text("UPDATE datatable SET business_unit = :business_unit, ship = :ship, tve = :tve, part_number = :part_number, description = :description, assembly = :assembly, qty = :qty, code = :code, owner = :owner, need_date = :need_date, ecd = :ecd, previous_ecd = :previous_ecd, impact = :impact, comment = :comment, status = :status, last_edit = :last_edit, added_date = :added_date, on_board = :on_board, closed_date = :closed_date, manager = :manager, ntid = :ntid WHERE id = :id")
    con.execute(update_query, {
        'business_unit': data['business_unit'], 'ship': data['ship'], 'tve': data['tve'], 'part_number': data['part_number'], 'description': data['description'], 'assembly': data['assembly'], 'qty': data['qty'], 'code': data['code'], 'owner': data['owner'], 'need_date': data['need_date'], 'ecd': data['ecd'], 'previous_ecd': data['previous_ecd'], 'impact': data['impact'], 'comment': data['comment'], 'status': data['status'], 'last_edit': data['last_edit'], 'added_date': data['added_date'], 'on_board': data['on_board'], 'closed_date': data['closed_date'], 'manager': data['manager'], 'ntid': data['ntid'], 'id': _id})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"Data was successfully updated. id": _id}), 200


@app.route('/datatable/<int:_id>', methods=['DELETE'])
@cross_origin()
def delete_data(_id):
    delete_query = text("DELETE FROM datatable WHERE id = :id")
    con.execute(delete_query, {'id': _id})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"Data was successfully deleted. id": _id}), 200
