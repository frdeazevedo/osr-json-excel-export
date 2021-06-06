import json, xlsxwriter, sys, os

# Converts lap time in milliseconds to human readable string
def msToLapTime(ms:int):
    hours = ms/3600000
    mins = (hours%1)*60
    secs = (mins%1)*60
    milli = (secs%1)*1000

    hours = int(hours)
    mins = int(mins)
    secs = int(secs)
    milli =int(milli)

    str_hours = str(hours)
    str_mins = str(mins)
    str_secs = str(secs)
    str_milli =str(milli)

    if hours < 10:
        str_hours = '0'+str(hours)

    if mins < 10:
        str_mins = '0'+str(mins)
    
    if secs < 10:
        str_secs = '0'+str(secs)
    
    if milli < 10:
        str_milli = '00'+str(milli)
    elif milli < 100:
        str_milli = '0'+str(milli)

    if hours > 0:
        return str_hours+":"+str_mins+":"+str_secs+":"+str_milli
    else:
        return str_mins+":"+str_secs+":"+str_milli

# [{name}, {lap_counter}, {lap_time}, {time}], [{name}, {lap_counter}, {lap_time}, {time}], 
def sortLapTimes(lap_times):
    return sorted(lap_times, key=lambda x:x['lap_time'])

# sometimes the json brings a dictionary, other times a list, couldn't figure out the logic behind it...
def searchParticipant(participants, refid):
    if type(participants) == dict:
        p_json = json.loads(json.dumps(participants, indent=4))
        
        for key, value in p_json.items():
            if p_json[key].get('RefId') == refid:
                return p_json[key]
    elif type(participants) == list:
        for p in participants:
            if p.get('RefId') == refid:
                return p

# stats > history > stages > practice1
# orders from fastest to slowest lap for each history
def getHistoryList(json_obj):
    history_list = []
    history = json_obj['stats']['history']

    for h in history:
        if 'practice1' in h['stages']:
            practice1_lap_times = []
            practice1_events = h['stages']['practice1']['events']
            participants = h['participants']
            for event in practice1_events:
                if 'CountThisLapTimes' in event['attributes']:
                    if (event['attributes']['CountThisLapTimes'] == 1
                        and event['attributes']['Sector1Time'] != 0
                        and event['attributes']['Sector2Time'] != 0
                        and event['attributes']['Sector3Time'] != 0):
                        lap_counter = event['attributes']['Lap']
                        lap_time = event['attributes']['LapTime']
                        name = event['name']
                        time = event['time']
                        participant = searchParticipant(participants, event['refid'])
                        laps_turned = getLaps(practice1_events, event['refid'])
                        vehicle = participant.get('VehicleId')
                        practice1_lap_times.append({'laps_turned':laps_turned, 'name':name, 'lap_counter':lap_counter, 'lap_time':lap_time, 'time':time, 'vehicle':vehicle})
            history_list.append(sortLapTimes(practice1_lap_times))
    
    return history_list

def getAllHistoryLaps(history_list):
    laps = []
    for h in history_list:
        for l in h:
            laps.append(l)
    
    return sortLapTimes(laps)

# laps has to be already ordered from fastest to slowest
def getFastestLaps(laps):
    fastest_laps = []
    recorded_drivers = []

    for l in laps:
        if l['name'] not in recorded_drivers:
            recorded_drivers.append(l['name'])
            fastest_laps.append(l)

    return fastest_laps

def getVehicle(vehicles_json, vehicleId):
    for vehicle in vehicles_json:
        if vehicle['id'] == vehicleId:
            return vehicle

def exportToXLSX(laps):
    current_dir = os.path.dirname(os.path.realpath('__file__'))
    vehicles_file = os.path.join(current_dir, 'resources/vehicle_list.json')

    with open(vehicles_file, encoding='utf-8') as json_file:
        json_data = json_file.read()
    
    vehicles_json_obj = json.loads(json_data)

    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['Position', 'Driver', 'Vehicle', 'Laps', 'Best Lap'])

    pos = 1
    for l in laps:
        vehicle = getVehicle(vehicles_json_obj, l['vehicle'])
        worksheet.write_row(pos, 0, [pos, l['name'], vehicle['name'], l['laps_turned'], msToLapTime(l['lap_time'])])
        pos = pos+1
    
    workbook.close()

def getLaps(events, refid):
    counter = 0
    for e in events:
        if 'CountThisLapTimes' in e['attributes']:
            if e['attributes']['CountThisLapTimes']==1 and e['refid']==refid and e['attributes']['Sector1Time'] != 0 and e['attributes']['Sector2Time'] != 0 and e['attributes']['Sector3Time'] != 0:
                counter = counter+1
    
    return counter

def main():
    if len(sys.argv) != 2:
        print("Error: expected 1 argument, but "+str(len(sys.argv))+" was/were given.")
        print("Usage:\n    osr_export <path/to/file.json>")
        return -1

    current_dir = os.path.dirname(os.path.realpath('__file__'))
    #test_data_file = os.path.join(current_dir, 'src/tests/test-data.json')
    data_file = os.path.join(current_dir, sys.argv[1])

    with open(data_file, encoding='utf-8') as json_file:
        json_data = json_file.read()

    json_obj = json.loads(json_data)

    history = getHistoryList(json_obj)

    fastest_laps = getFastestLaps(getAllHistoryLaps(history))
    for fl in fastest_laps:
        print(msToLapTime(fl['lap_time'])+" "+fl['name'])

    exportToXLSX(fastest_laps)
    
main()