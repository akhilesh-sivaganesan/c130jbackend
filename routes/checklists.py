from datetime import datetime as dt
from flask import jsonify, request, abort
import sqlalchemy
from sqlalchemy.sql import text
from flask_cors import cross_origin
from config import app, con

# Get all checklists and their nodes


@app.route('/checklists', methods=['GET'])
@cross_origin()
def handle_checklists():
    select_query = text('SELECT * FROM osf_public.checklists')
    rs = con.execute(select_query)
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text(
            'SELECT * FROM osf_public.checklist_nodes WHERE checklist_id = ' + "\'" + tempDict['checklist_id'] + "\'")
        result = con.execute(select_query)
        resultS = result.fetchall()
        tempDict['checklist_nodes'] = [
            dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200

@app.route('/checklists/user/<string:user_id>', methods=['GET'])
@cross_origin()
def get_checklists_by_user(user_id):
    select_query = text(
        'SELECT * FROM osf_public.checklists WHERE user_id = :user_id')
    rs = con.execute(select_query, {'user_id': user_id})
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text(
            'SELECT * FROM osf_public.checklist_nodes WHERE checklist_id = :checklist_id')
        result = con.execute(select_query, {'checklist_id': tempDict['checklist_id']})
        resultS = result.fetchall()
        tempDict['checklist_nodes'] = [
            dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200

# Get a checklist and its nodes by checklist_ID


@app.route('/checklists/<string:_id>', methods=['GET'])
@cross_origin()
def get_checklist_by_id(_id):
    select_query = text(
        f'SELECT * FROM osf_public.checklists WHERE checklist_id = :id')
    rs = con.execute(select_query, {'id': _id})
    row = rs.fetchone()
    if row is None:
        abort(404)
    result = dict(row._mapping.items())
    select_query = text(
        'SELECT * FROM osf_public.checklist_nodes WHERE checklist_id = :id ORDER BY checklist_node_index')
    resultS = con.execute(select_query, {'id': _id})
    result['checklist_nodes'] = [dict(t._mapping.items()) for t in resultS]
    final_response = jsonify(result)
    return final_response, 200

# Create a new checklist and its nodes


@app.route('/checklists', methods=['POST'])
@cross_origin()
def create_form_checklist():
    data = request.get_json(force=True)
    insert_query = text("INSERT INTO osf_public.checklists (checklist_id, checklist_title, user_id, checklist_created_at, checklist_completion_timestamp, checklist_completion) VALUES (:checklist_id, :checklist_title, :user_id, :checklist_created_at, :checklist_completion_timestamp, :checklist_completion)")
    con.execute(insert_query, {
        'checklist_id': data['checklist_id'],
        'checklist_title': data['checklist_title'],
        'user_id': data['user_id'],
        'checklist_created_at': data['checklist_created_at'],
        'checklist_completion_timestamp': data['checklist_completion_timestamp'] if data['checklist_completion_timestamp'] else None,
        'checklist_completion': data['checklist_completion']
    })

    for ditem in data['checklist_nodes']:
        insert_query = text("INSERT INTO osf_public.checklist_nodes (checklist_node_id, checklist_node_title, checklist_node_description, checklist_node_type, checklist_id, checklist_node_completion, checklist_node_completion_timestamp, checklist_node_index, checklist_node_data_url, qr_code) VALUES (:checklist_node_id, :checklist_node_title, :checklist_node_description, :checklist_node_type, :checklist_id, :checklist_node_completion, :checklist_node_completion_timestamp, :checklist_node_index, :checklist_node_data_url, :qr_code)")
        con.execute(insert_query, {
            'checklist_node_id': ditem['checklist_node_id'],
            'checklist_node_title': ditem['checklist_node_title'],
            'checklist_node_description': ditem['checklist_node_description'],
            'checklist_node_type': ditem['checklist_node_type'],
            'checklist_id': ditem['checklist_id'],
            'checklist_node_completion': ditem['checklist_node_completion'],
            'checklist_node_completion_timestamp': ditem['checklist_node_completion_timestamp'] if ditem['checklist_node_completion_timestamp'] else None,
            'checklist_node_index': ditem['checklist_node_index'],
            'checklist_node_data_url': ditem['checklist_node_data_url'],
            'checklist_node_feedback': ditem['checklist_node_feedback'],
            'qr_code': ditem['qr_code']
        })

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 201 Created
    return jsonify({"checklist was successfully created. checklist_id": data['checklist_id']}), 201


# Update a checklist and its nodes
@app.route('/checklists/<string:_id>', methods=['PUT'])
@cross_origin()
def update_checklist(_id):
    data = request.get_json(force=True)
    update_query = text("UPDATE osf_public.checklists SET checklist_title = :title, user_id = :user_id, checklist_created_at = :created_at, checklist_completion_timestamp = :completion_timestamp, checklist_completion = :completion WHERE checklist_id = :id")
    con.execute(update_query, {'title': data['checklist_title'], 'user_id': data['user_id'], 'created_at': data['checklist_created_at'],
                'completion_timestamp': data['checklist_completion_timestamp'], 'completion': data['checklist_completion'], 'id': _id})

    for ditem in data['checklist_nodes']:
        update_query = text("UPDATE osf_public.checklist_nodes SET checklist_node_title = :title, checklist_node_description = :description, checklist_node_type = :type, checklist_id = :checklist_id, checklist_node_completion = :completion, checklist_node_completion_timestamp = :completion_timestamp, checklist_node_index = :checklist_node_index, checklist_node_data_url = :checklist_node_data_url, checklist_node_feedback = :checklist_node_feedback, qr_code = :qr_code WHERE checklist_node_id = :id")
        con.execute(update_query, {'title': ditem['checklist_node_title'], 'description': ditem['checklist_node_description'], 'type': ditem['checklist_node_type'], 'checklist_id': ditem['checklist_id'],
    'completion': ditem['checklist_node_completion'], 'completion_timestamp': ditem['checklist_node_completion_timestamp'] if ditem['checklist_node_completion_timestamp'] else None, 'checklist_node_index': ditem['checklist_node_index'], 'id': ditem['checklist_node_id'], 'checklist_node_data_url': ditem['checklist_node_data_url'], 'checklist_node_feedback': ditem['checklist_node_feedback'], 'qr_code': ditem['qr_code']})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"checklist was successfully updated. checklist_id": _id}), 200


# Delete a checklist and its nodes


@app.route('/checklists/<string:_id>', methods=['DELETE'])
@cross_origin()
def delete_checklist(_id):
    delete_query = text(
        "DELETE FROM osf_public.checklist_nodes WHERE checklist_id = :id")
    con.execute(delete_query, {'id': _id})

    delete_query = text(
        "DELETE FROM osf_public.checklists WHERE checklist_id = :id")
    con.execute(delete_query, {'id': _id})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"checklist was successfully deleted. checklist_id": _id}), 200

@app.route('/checklists/qr-code', methods=['PUT'])
@cross_origin()
def update_checklist_node_by_qr_code():
    data = request.get_json(force=True)
    qr_code = data['qr_code']
    checklist_node_id = data['checklist_node_id']

    # Check if the qr_code exists in the template_nodes table
    select_query = text(
        "SELECT * FROM osf_public.template_nodes WHERE qr_code = :qr_code")
    result = con.execute(select_query, {'qr_code': qr_code}).fetchone()

    if result:
        # Check if the qr_code field for the checklist_node object matches the QR code sent in the request
        select_query = text(
            "SELECT * FROM osf_public.checklist_nodes WHERE checklist_node_id = :id AND qr_code = :qr_code")
        result = con.execute(select_query, {'id': checklist_node_id, 'qr_code': qr_code}).fetchone()

        if result:
            # Update the checklist node
            update_query = text(
                "UPDATE osf_public.checklist_nodes SET checklist_node_completion = :completion, checklist_node_completion_timestamp = :completion_timestamp WHERE checklist_node_id = :id")
            con.execute(update_query, {
                'completion': True,
                'completion_timestamp': dt.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                'id': checklist_node_id
            })

            # Get the checklist_id from the checklist_node
            select_query = text(
                "SELECT checklist_id FROM osf_public.checklist_nodes WHERE checklist_node_id = :id")
            result = con.execute(select_query, {'id': checklist_node_id}).fetchone()
            if result:
                checklist_id = result[0]

                # Check if all the nodes in the checklist are completed
                select_query = text(
                    "SELECT * FROM osf_public.checklist_nodes WHERE checklist_id = :id AND checklist_node_completion = false")
                result = con.execute(select_query, {'id': checklist_id}).fetchone()
                if not result:
                    # All nodes are completed, update the checklist
                    update_query = text(
                        "UPDATE osf_public.checklists SET checklist_completion = true, checklist_completion_timestamp = :timestamp WHERE checklist_id = :id")
                    con.execute(update_query, {
                        'timestamp': dt.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                        'id': checklist_id
                    })

            commit_text = text("COMMIT;")
            con.execute(commit_text)

            # HTTP 200 OK
            return jsonify({"checklist node was successfully updated. checklist_node_id": checklist_node_id}), 200
        else:
            # HTTP 400 Bad Request
            return jsonify({
                "error": "Wrong QR code scanned",
                "data_received": {
                    "qr_code": qr_code,
                    "checklist_node_id": checklist_node_id
                },
                "checklist_nodes_query_result": result
            }), 400
    else:
        # HTTP 400 Bad Request
        return jsonify({
            "error": "Invalid qr_code",
            "data_received": {
                "qr_code": qr_code,
                "checklist_node_id": checklist_node_id
            },
            "template_nodes_query_result": result
        }), 400
