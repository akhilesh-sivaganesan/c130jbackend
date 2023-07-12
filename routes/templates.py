from flask import jsonify, request, abort
import sqlalchemy
from sqlalchemy.sql import text
from flask_cors import cross_origin
from config import app, con

# Get all templates and their nodes


@app.route('/templates', methods=['GET'])
@cross_origin()
def handle_forms():
    select_query = text('SELECT * FROM osf_public.templates')
    rs = con.execute(select_query)
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text(
            'SELECT * FROM osf_public.template_nodes WHERE template_id = ' + "\'" + tempDict['template_id'] + "\'")
        result = con.execute(select_query)
        resultS = result.fetchall()
        tempDict['template_nodes'] = [
            dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200

# Get a template and its nodes by template_ID


@app.route('/templates/<string:_id>', methods=['GET'])
@cross_origin()
def get_template_by_id(_id):
    select_query = text(
        f'SELECT * FROM osf_public.templates WHERE template_id = :id')
    rs = con.execute(select_query, {'id': _id})
    row = rs.fetchone()
    if row is None:
        abort(404)
    result = dict(row._mapping.items())
    select_query = text(
        'SELECT * FROM osf_public.template_nodes WHERE template_id = :id ORDER BY node_index')
    resultS = con.execute(select_query, {'id': _id})
    result['template_nodes'] = [dict(t._mapping.items()) for t in resultS]
    final_response = jsonify(result)
    return final_response, 200

@app.route('/templates/user/<string:user_id>', methods=['GET'])
@cross_origin()
def get_templates_by_user(user_id):
    select_query = text(
        'SELECT * FROM osf_public.templates WHERE template_owner_id = :user_id')
    rs = con.execute(select_query, {'user_id': user_id})
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text(
            'SELECT * FROM osf_public.template_nodes WHERE template_id = :template_id')
        result = con.execute(select_query, {'template_id': tempDict['template_id']})
        resultS = result.fetchall()
        tempDict['template_nodes'] = [
            dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200

@app.route('/templates/assigned/<string:user_id>', methods=['GET'])
@cross_origin()
def get_assigned_templates(user_id):
    select_query = text(
        'SELECT * FROM osf_public.templates WHERE template_assigned_to = :user_id')
    rs = con.execute(select_query, {'user_id': user_id})
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text(
            'SELECT * FROM osf_public.template_nodes WHERE template_id = :template_id')
        result = con.execute(select_query, {'template_id': tempDict['template_id']})
        resultS = result.fetchall()
        tempDict['template_nodes'] = [
            dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    return final_response, 200


# Create a new template and its nodes


@app.route('/templates', methods=['POST'])
@cross_origin()
def create_form_template():
    data = request.get_json(force=True)
    insert_query = text("INSERT INTO osf_public.templates (template_id, template_title, template_owner_id, template_created_at) VALUES ('% s', '% s', '% s', '% s');" % (
        data['template_id'], data['template_title'], data['template_owner_id'], data['template_created_at']))
    con.execute(insert_query)

    for ditem in data['template_nodes']:
        insert_query = text("INSERT INTO osf_public.template_nodes (node_id, node_title, node_description, node_type, template_id, node_index, qr_code) VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s');" % (
            ditem['node_id'], ditem['node_title'], ditem['node_description'], ditem['node_type'], ditem['template_id'], ditem['node_index'], ditem['qr_code']))
        con.execute(insert_query)

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 201 Created
    return jsonify({"Template was successfully created. template_id": data['template_id']}), 201

# Update a template and its nodes


@app.route('/templates/<string:_id>', methods=['PUT'])
@cross_origin()
def update_template(_id):
    data = request.get_json(force=True)
    update_query = text(
        "UPDATE osf_public.templates SET template_title = :title, template_owner_id = :owner_id, template_created_at = :created_at WHERE template_id = :id")
    con.execute(update_query, {
                'title': data['template_title'], 'owner_id': data['template_owner_id'], 'created_at': data['template_created_at'], 'id': _id})

    # Need to update so that different node list is POSTed to database, cannot overwrite

    delete_query = text(
        "DELETE FROM osf_public.template_nodes WHERE template_id = :id")
    con.execute(delete_query, {'id': _id})

    for ditem in data['template_nodes']:
        insert_query = text("INSERT INTO osf_public.template_nodes (node_id, node_title, node_description, node_type, template_id, node_index, qr_code) VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s');" % (
            ditem['node_id'], ditem['node_title'], ditem['node_description'], ditem['node_type'], ditem['template_id'], ditem['node_index'], ditem['qr_code']))
        con.execute(insert_query)

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"Template was successfully updated. template_id": _id}), 200

@app.route('/templates/<string:_id>/assign', methods=['PUT'])
@cross_origin()
def update_template_assigned_to(_id):
    data = request.get_json(force=True)
    update_query = text(
        "UPDATE osf_public.templates SET template_assigned_to = :assigned_to WHERE template_id = :id"
    )
    con.execute(update_query, {'assigned_to': data['template_assigned_to'], 'id': _id})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"Template was successfully updated. template_id": _id}), 200

# Delete a template and its nodes


@app.route('/templates/<string:_id>', methods=['DELETE'])
@cross_origin()
def delete_template(_id):
    delete_query = text(
        "DELETE FROM osf_public.template_nodes WHERE template_id = :id")
    con.execute(delete_query, {'id': _id})

    delete_query = text(
        "DELETE FROM osf_public.templates WHERE template_id = :id")
    con.execute(delete_query, {'id': _id})

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 200 OK
    return jsonify({"Template was successfully deleted. template_id": _id}), 200
