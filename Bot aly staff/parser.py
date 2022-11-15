from pipedream.script_helpers import (steps, export)
import re

all_events = []


pds_id = "1036381708968263744"


for event in steps["trigger"]["event"]:
  if event["channel_id"] == pds_id:
    print("pds")
    text = event["content"]

    pattern = '\*\*(.*)\*\* a pris son service'
    name = re.search(pattern, text, re.IGNORECASE).group(1)

    pattern = 'a pris son service qui a duré : ([0-9]{1,}) Heures'
    heures = re.search(pattern, text, re.IGNORECASE).group(1)

    pattern = 'a pris son service qui a duré : [0-9]{1,} Heures ([0-9]{1,}) Minutes'
    minutes = re.search(pattern, text, re.IGNORECASE).group(1)

    nb_heure = round((((int(heures) * 3600) + (int(minutes) * 60)) / 3600), 2)

    if(nb_heure > 0):
      all_events.append([event["timestamp"], "pds", name, nb_heure])



# Return data for use in future steps
export("all_events",  all_events)