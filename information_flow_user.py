import copy
import sys

from pm4py.objects.log.importer.xes import importer as xes_importer

from pm4py.algo.filtering.log.attributes import attributes_filter

log = xes_importer.apply('BPI_2017_all1.xes')
print(log)

def find_first_event(case,attribute_starts):
    for event in case:
        if event["concept:name"].startswith(attribute_starts):
            return event
            break

def find_first_event_not(case,attribute_starts):
    for event in case:
        if not event["concept:name"].startswith(attribute_starts):
            return event
            break


for case in log:
    old_event = find_first_event(case,"O_")
    if old_event == None:
        continue
    last_found_index = -1
    for i, event in enumerate(case):
        if event["concept:name"].startswith("O_"):
            if event["org:resource"] != old_event["org:resource"]:
                index_target = i
                source_found = False
                for j, event_b in enumerate(case):
                    if j == index_target:
                        break
                    if (not event_b["concept:name"].startswith("O_")) and event_b["org:resource"] == event["org:resource"] and j > last_found_index:
                        source_event = event_b
                        source_found = True
                        last_found_index = j
                if source_found:
                    intermediate_event = copy.deepcopy(source_event)
                    intermediate_event["concept:name"] = source_event["concept:name"] +"_" + event["concept:name"]
                    timedelta = (event["time:timestamp"] - source_event["time:timestamp"])/2
                    intermediate_event["time:timestamp"] = source_event["time:timestamp"] + timedelta
                    file = open('resource.csv', 'a')
                    sys.stdout = file
                    print(case.attributes["concept:name"], ",", source_event["time:timestamp"], ",",
                          source_event["concept:name"])
                    print(case.attributes["concept:name"], ",", intermediate_event["time:timestamp"], ",",
                          intermediate_event["concept:name"])
                    print(case.attributes["concept:name"], ",", event["time:timestamp"], ",", event["concept:name"])
                    file.close()
            old_event=event





