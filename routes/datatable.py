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
        # Convert ntid from string to array
        if tempDict['ntid'] is None:
            tempDict['ntid'] = []
        else:
            tempDict['ntid'] = tempDict['ntid'].split(',')
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
        # Convert ntid from string to array
        if tempDict['ntid'] is None:
            tempDict['ntid'] = []
        else:
            tempDict['ntid'] = tempDict['ntid'].split(',')
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
        # Convert ntid from string to array
        if tempDict['ntid'] is None:
            tempDict['ntid'] = []
        else:
            tempDict['ntid'] = tempDict['ntid'].split(',')
        duration_days = datetime.now() - tempDict['added_date']
        if tempDict['closed_date']:
            duration_days = tempDict['closed_date'] - tempDict['added_date']
        tempDict['duration_days'] = duration_days.days
        if not tempDict['last_edit']:
            tempDict['last_edit'] = tempDict['added_date']
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
    # Convert ntid from array to string
    data['ntid'] = ','.join(data['ntid'])
    insert_query = text("INSERT INTO datatable (business_unit, ship, tve, part_number, description, assembly, qty, code, owner, need_date, ecd, previous_ecd, impact, comment, status, last_edit, added_date, on_board, closed_date, manager, ntid) VALUES (:business_unit,:ship,:tve,:part_number,:description,:assembly,:qty,:code,:owner,:need_date,:ecd,NULL,:impact,:comment,:status,:last_edit,:added_date,:on_board,NULL,:manager,:ntid) RETURNING id;")
    result = con.execute(insert_query,data)
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
    # Convert ntid from array to string
    data['ntid'] = ','.join(data['ntid'])
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

def parse_date(date_str):
    if not date_str or date_str == 'DLVD' or date_str == 'W/A':
        return None
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except Exception as error:
        print(error)
        return None
    

def parse_int(int_str):
    if not int_str:
        return None
    return int(int_str)

@app.route('/datatable/sync', methods=['POST'])
def sync():
        data = request.get_json(force=True)
        # print(data)
        # Insert data into Postgres table
        for index, row in enumerate(data):
            if not row['business_unit']:
                continue
            try:
                # if index == 0:
                #     print(row)
                # Validate data
                row['closed_date'] = parse_date(row['closed_date'])
                row['last_edit'] = parse_date(row['last_edit'])
                row['need_date'] = parse_date(row['need_date'])
                row['qty'] = parse_int(row['qty'])
                row['ecd'] = parse_date(row['ecd'])
                row['added_date'] = parse_date(row['added_date'])
                row['status'] = row['status'].upper()

                # Check if previous_ecd is present in row
                if 'previous_ecd' not in row:
                    row['previous_ecd'] = None
                else:
                    row['previous_ecd'] = parse_date(row['previous_ecd'])
                # Check if ntid is present in row
                if 'ntid' not in row:
                    row['ntid'] = None

                select_stmt = text('SELECT * FROM osf_public.datatable WHERE business_unit=:business_unit AND ship=:ship AND tve=:tve AND part_number=:part_number AND description=:description AND assembly=:assembly AND qty=:qty AND code=:code AND owner=:owner AND need_date=:need_date AND ecd=:ecd AND impact=:impact AND comment=:comment AND status=:status AND last_edit=:last_edit AND added_date=:added_date AND on_board=:on_board AND closed_date=:closed_date AND manager=:manager')
                result = con.execute(select_stmt, row).fetchone()
                if not result:
                    # Create insert statement
                    insert_stmt = text('INSERT INTO osf_public.datatable (business_unit, ship, tve, part_number, description, assembly, qty, code, owner, need_date, ecd, impact, comment, status, last_edit, added_date, on_board, closed_date, manager, ntid, previous_ecd) VALUES (:business_unit,:ship,:tve,:part_number,:description,:assembly,:qty,:code,:owner,:need_date,:ecd,:impact,:comment,:status,:last_edit,:added_date,:on_board,:closed_date,:manager,:ntid,:previous_ecd)')
                    # Execute insert statement
                    con.execute(insert_stmt,row)
                    commit_text = text("COMMIT;")
                    con.execute(commit_text)
            except Exception as error:
                print('Here error', error)
                print('Here index', index)
                print('here row', row)
                return 'An error occurred while syncing data', 500
        return 'Data synced successfully', 200
    



