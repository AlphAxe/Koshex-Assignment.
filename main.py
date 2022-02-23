from flask import jsonify,request
from database import query,Url,randomize,initialize_app
from datetime import datetime

# creating Flask app object
app = initialize_app()

#api that will take an url and return its short url ,number of hits and hourly basis hits
@app.route("/url/",methods=["POST"])
def url():
    try:
        current_hour = datetime.now().hour
        response = {}
        data = request.json                                     # accepting data from body
        url = data.get('url')
        filter_params = {'url': url}
        # querying database to check if url already exists or not in database
        obj = query.select(Url, filter_params=filter_params)    # query object
        if not obj:                                             #condition to check if no such url in database is present
            short_url = randomize()                             # creating short url with the function imported from database.py
            date_created = datetime.now()
            insert_params = {'url':url,'short_url':short_url,'date_created':date_created,'count':0,'hourly_count':0} #inserting url details in database table named as url
            query.insert(Url,insert_params = insert_params)
            response['short_url'] = short_url
            filter_params = {'short_url':short_url}             # querying database to make a response need to be send with all necessary details
            obj = query.select(Url, filter_params=filter_params)
            response['count'] = obj.count
            response['hourly_count'] = obj.hourly_count

        else:                                   # condition if url is already present in database
            last_hour = (obj.date_created).hour # accessing hour from database table for the given url
            count = obj.count + 1               # incrementing number of hits if Url already present in database
            if abs(current_hour - last_hour) == 1: # condition to check if one hour is passed to count number of hits on hourly basis
                hourly_count = obj.hourly_count+1
            else:                                  # condition if one hour is not crossed
                hourly_count = obj.hourly_count
            update_params = {'count':count,'hourly_count':hourly_count}
            filter_params = {'url':obj.url}
            query.update(Url, update_params=update_params,filter_params=filter_params) # updating hits and hourly hits in database
            # making response to be send with necessary details
            response['short_url'] = obj.short_url
            response['count'] = count
            response['hourly_count'] = hourly_count

    except Exception as e_:
        return jsonify({"message":e_})
    return jsonify(response)


#api that will return the original url of the short url
@app.route("/<short_url>",methods=["GET"])
def short_url(short_url):
    try:
        response ={}
        filter_params = {'short_url':short_url}              # filter parameters to query database table url
        obj = query.select(Url, filter_params=filter_params) # query object
        if not obj:
            response['message'] = 'No data available'
            return jsonify(response)
        else: # making response to send original url of short version
            original_url = obj.url
            response['original_url'] = original_url
            return jsonify(response)
    except Exception as e_:
        return jsonify({"message":e_})








