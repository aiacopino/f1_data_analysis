import fastf1, fastf1.plotting
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache') #enable caching of data

#session types: Q qualif, R race, FP1, FP2, FP3 free practice, S sprint race
race_1 = fastf1.get_session(2023, 'Monaco', 'Q') # qualifying data for Monaco 2023
race_1.load()
race_2 = fastf1.get_session(2023, 'Monaco', 'R') #race data for Monaco 2023
race_2.load() 

all_drivers = race_1.results['Abbreviation'].unique() #array of unique vals
top_5_drivers = race_2.results['Abbreviation'][:5].tolist() #list of top 5 (for filtering below)

print(f"Drivers in the qualifying session:{list(all_drivers)}")
print(f"Top 5 in final race: {list(top_5_drivers)}")

plt.figure(figsize=(12,6))

for drv in all_drivers:
    alpha=.3
    if drv in top_5_drivers: #print only top 5 with full opacity
        alpha=1
    try:
        qualif_lap = race_1.laps.pick_drivers(drv).pick_fastest()
        race_lap = race_2.laps.pick_drivers(drv).pick_fastest()
        telemetry_qualif = qualif_lap.get_telemetry().add_distance()
        telemetry_race = race_lap.get_telemetry().add_distance()
        filter_curve=(telemetry_race['Distance'] >= 1600) & (telemetry_race['Distance'] <= 2000) #filter only the curve section of the track where differences are biggest
        segment = telemetry_race.loc[filter_curve]
        #plt.plot(telemetry_qualif['Distance'], telemetry_qualif['Speed'], label=f'{drv} Qualif', linestyle='--', alpha=alpha)
        #plt.plot(telemetry_race['Distance'], telemetry_race['Speed'], label=f'{drv}', linestyle='-', alpha=alpha)
        plt.plot(segment['Distance'], segment['Speed'], label=f'{drv}', linestyle='-', alpha=alpha)
    except Exception as e:
        print(f"Could not retrieve data for driver {drv}: {e}")
        continue

# custom legend sorting
handles, labels = plt.gca().get_legend_handles_labels() #get current axes, names of drawn lines # handles = color lines, labels = abbreviations
driver_order = {drv: i+1 for i, drv in enumerate(race_2.results['Abbreviation'])} #enum drivers in descending speed of final race order
sorted_pairs = sorted(zip(handles, labels), key=lambda x: driver_order[x[1]]) #sort list of tuples(abbreviation, handle(=line)) by driver order
sorted_handles, sorted_labels = zip(*sorted_pairs) # unzip

plt.title('Top 5 Drivers: Qualifying vs Race Speeds - Monaco 2023')
plt.xlabel('Distance (m)')
plt.ylabel('Speed (km/h)')
plt.legend(sorted_handles, sorted_labels, title='Finishing Order Descending', loc='upper left', bbox_to_anchor=(0,1))
plt.grid(True, alpha=.3)
plt.show()