def get_record(model, record_id):
    record = model.query.get(record_id)

    return record
