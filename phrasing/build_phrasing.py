"""Source for phrasing.csv: every piece of wording in the app and the conditions it appears under.
Run:  python3 phrasing/build_phrasing.py
The CSV is published with the site (https://www.checkthewind.com/phrasing.csv) and the Google Sheet
"Check the Wind - Phrasing and Conditions (formatted)" reads it with =IMPORTDATA(...).
Keep this file in step with index.html: change wording there, change the matching row here.
"""
import csv
R=[]
def a(area,where,phrase,when,notes=''): R.append([area,where,phrase,when,notes])

T='Verdict tag'
tw='Tag pill'
a(T,tw,'Go Outside!','Verdict is Yes: the current hour passes every limit and scores well (score 0.5 or higher), with no Severe/Extreme alert.','Green')
a(T,tw,'Okay for Now','Verdict is Maybe and the window starts now: the current hour passes the limits but is not ideal.','Yellow')
a(T,tw,'Wait a Bit','Verdict is Maybe and a good window starts later today.','Yellow')
a(T,tw,'Stay Inside','Verdict is No right now, but a good window exists within the next 48 hours (not later today).','Orange')
a(T,tw,'Stay In','Verdict is No and there is no good window in the next 48 hours.','Red')
a(T,tw,'Use Caution','A Severe or Extreme National Weather Service alert is active and the verdict is not No (a Yes is downgraded to Maybe).','Orange; takes priority over the other tags unless the verdict is No')
a(T,tw,'Night Time','Darkness is the ONLY reason the hour is ruled out, wind is under 16 mph, no Severe/Extreme alert, and the verdict is not Yes.','Purple with a moon')
a('Verdict word','Verdict card (details)','Yes / Maybe / No','Matches the verdict state above.','Also shows the time range (e.g. "from now until 6 PM"); "Right now" when No')

S='One-line summary'
sw='Verdict card, first sentence'
a(S,sw,'[Freezing/Cold/Cool/Mild/Warm/Hot], [calm/breezy/windy/blustery/howling] and [dry/damp/wet], with [clean/moderate] air.','Verdict is Yes (no alert).','Feel from average temp: under 32 freezing, under 45 cold, under 58 cool, under 72 mild, under 85 warm, otherwise hot. Wind from the top wind in the window (see Wind categories). Ground: under 0.15 dry, under 0.45 damp, else wet. Air: AQI 50 or less is "clean air", higher is "moderate air"; left out if AQI is unknown.')
a(S,sw,'Okay for now, but not ideal: [weak points].','Verdict is Maybe and the window starts now.','Up to 2 weak points (see Weak points).')
a(S,sw,'Not right now — [reasons]. Later: [the Yes sentence, lowercased]','Verdict is Maybe with a window later today.','Up to 2 reasons (see Reasons a time is ruled out).')
a(S,sw,'Better to skip it for now: [reasons].','Verdict is No.','Up to 2 reasons; a Severe/Extreme alert is listed first as "an active [alert]".')
a(S,sw,'Conditions look fine, but there’s an active [alert]. Be careful.','Severe/Extreme alert and the verdict is Yes or Maybe.','Replaces the lines above')
a(S,'Verdict card, below the sentence','Next good window: [range].','Verdict is No and a good window exists within 48 hours.')
a(S,'Verdict card, below the sentence','No good window in the next 48 hours.','Verdict is No and no window exists.')
a(S,'Verdict card, bottom','Active alert: [event]. Check the details before heading out.','Any active alert that is NOT Severe/Extreme (e.g. an advisory).')

W='Weak points'
for ph,wh in [('wind up to [N] mph','Top wind in the window is 16 mph or more.'),('chilly at [N]°F','Average temp under 40°F.'),('hot at [N]°F','Average temp over 88°F.'),('[N]% chance of precipitation','Chance of precipitation is 30% or more.'),('damp ground','Ground wetness is 0.15 or more.'),('moderate air quality','AQI is above 50.')]:
    a(W,'Okay for Now text',ph,wh)

Rs='Reasons a time is ruled out'
for ph,wh,n in [('it’s dark out','No daylight at that hour (uses real sunrise/sunset).',''),
 ('thunderstorms / snow / showers / rain','Forecast shows that precipitation type (not just a "chance of").',''),
 ('wind up to [N] mph','Wind at or above the Best Times wind limit.','Default limit 25 mph'),
 ('[N]% chance of precipitation','Chance at or above the limit.','Default limit 40%'),
 ('snowy or icy ground','Ice/snow in the forecast or on the ground.',''),
 ('cold at [N]°F','Below the minimum temperature.','Default 25°F'),
 ('hot at [N]°F','Above the maximum temperature.','Default 100°F'),
 ('poor air quality (AQI [N])','AQI above the limit.','Default limit 150'),
 ('high humidity','Humidity above the limit.','Default 100% (effectively off)'),
 ('wet ground','Ground wetness above the limit (only if the ground setting is on).','Off by default'),
 ('an active [alert]','Severe/Extreme alert is active.','Added to the front of the list')]:
    a(Rs,'Inside the No/Maybe text',ph,wh,n)

A='Activities line'
a(A,'Verdict card under the sentence','Good for [activity, activity and activity].','Yes or Maybe, with at least one activity that fits.','First 3 matching activities (short names)')
a(A,'Verdict card under the sentence','Fine for a short outing.','Yes or Maybe, but no listed activity fits.')
a(A,'Verdict card under the sentence','Better saved for indoor plans.','Verdict is No.')
a(A,'Verdict card under the sentence','Check the alert above before heading out.','Severe/Extreme alert and not No.')
a(A,'Verdict details (expanded)','A good time for indoor plans.','Verdict is No.')
a(A,'Verdict details (expanded)','Good for: [up to 5 activity names as chips]','Yes or Maybe; the chips use the full names in the Activities list.')
a(A,'Verdict details (expanded)','Stats: Temp / Wind / Precip / Air quality (Good, Moderate, Sensitive groups)','Always, for the verdict window.')

# activities
for name,verb,short,cond in [
 ('Walking','take a stroll','walking','Temp 32–92°F, wind under 25 mph, precip under 40%, AQI 100 or less'),
 ('Running','go for a run','running','Temp 28–78°F, wind under 20 mph, precip under 30%, AQI 100 or less'),
 ('Cycling','go for a bike ride','cycling','Temp 40–90°F, wind under 15 mph, precip under 20%, ground dry (under 0.15), AQI 100 or less'),
 ('Hiking','hit a trail','hiking','Temp 35–88°F, wind under 22 mph, precip under 30%, ground under 0.45, AQI 100 or less'),
 ('Fishing','go fishing','fishing','Temp 45–95°F, wind under 15 mph, precip under 30%, AQI 100 or less'),
 ('Golf','play a round of golf','golf','Temp 50–92°F, wind under 15 mph, precip under 20%, ground under 0.45, AQI 100 or less'),
 ('Swimming','take a swim','swimming','Low temp 78°F or higher, wind under 15 mph, precip under 20%, AQI 100 or less'),
 ('Sunbathing','soak up some sun','sunbathing','Temp 72–95°F, wind under 12 mph, precip under 15%, AQI 100 or less'),
 ('Hammock time','swing in a hammock','hammock time','Temp 58–88°F, wind under 10 mph, precip under 15%, AQI 100 or less'),
 ('Picnics & patio time','have a picnic','picnics','Temp 62–88°F, wind under 12 mph, precip under 20%, ground under 0.45, AQI 100 or less'),
 ('Gardening & yard work','putter in the garden','yard work','Temp 40–90°F, wind under 20 mph, precip under 30%, AQI 100 or less'),
 ('Kite flying','fly a kite','kite flying','Wind 8–24 mph throughout, precip under 30%, temp 32°F or higher'),
 ('Dog walks','walk your dog','dog walks','Temp 25–88°F, wind under 25 mph, precip under 40%, AQI 100 or less'),
 ('Bird watching','go bird watching','bird watching','Temp 35–90°F, wind under 15 mph, precip under 20%, AQI 100 or less'),
 ('Mowing the lawn','mow the lawn','mowing','Temp 50–92°F, wind under 20 mph, precip under 10%, ground dry (under 0.15), AQI 100 or less'),
 ('Pruning flowers','prune your flowers','pruning flowers','Temp 40–88°F, wind under 20 mph, precip under 30%, ground under 0.45, AQI 100 or less'),
 ('Washing the car','wash the car','car washing','Temp 50–95°F, wind under 20 mph, precip under 20%, AQI 100 or less'),
 ('Dining al fresco','dine al fresco','dining al fresco','Temp 58–90°F, wind under 12 mph, precip under 15%, AQI 100 or less')]:
    a('Activities','Chip / paragraph',f'{name}  |  short: {short}  |  verb: "{verb}"',cond,'Needs the whole window to fit (lowest/highest temp, top wind, highest precip chance)' if name.startswith('Walking') else '')

P='Paragraph (hero / verdict card)'
pw='Hero paragraph'
a(P,pw,'Conditions look good [from now until 6 PM / today 2 to 6 PM], but there’s an active [alert] for your area. [After-window sentence] Please be careful, and check the alert above before heading outside.','Severe/Extreme alert and verdict is Yes/Maybe.','"Conditions are okay" instead of "look good" when the verdict is the Okay-for-Now kind; "Conditions should be good [day] [time]" when the window is later.')
a(P,pw,'It’s best to stay inside for now: there is an active [alert] and [other reason]. Please stay safe, and check the alert above. Your next good window is [day time]. / There’s no good outdoor activity window in the next 48 hours, so it’s a fine time for a movie and a snack.','Severe/Extreme alert and the verdict is No.','Serious tone, no playful wording')
a(P,pw,'It’s a cozy-inside kind of moment right now: [reasons]. Your next good window is [day time], so it’s worth the wait. / There’s no good outdoor activity window in the next 48 hours, so it’s a fine time for a movie and a snack.','Verdict is No, no alert.','')
y1=['[Day] [time] is a lovely time to get outside.','Good news: [day] [time] is a great time to get outside.','Go on, get outside! [Day] [time] looks lovely.']
for s in y1: a(P,pw,s,'Verdict is Yes and it is comfortable (average 50–86°F, ground not wet).','One of three, chosen by the date')
for s in ['[Day] [time] is a good time to get outside.','Good news: [day] [time] works for getting outside.']: a(P,pw,s,'Verdict is Yes but not especially comfortable.','One of two, chosen by the date')
for s in ['It will be [the summary sentence, lowercased]','Expect [the summary sentence, lowercased]']: a(P,pw,s,'Verdict is Yes (second sentence).','One of two')
for s in ['This is great weather to [activities].','It’s a lovely time to [activities].','You could [activities].','Perfect conditions to [activities].']: a(P,pw,s,'Yes/Maybe with at least one fitting activity.','Up to 3 activity verbs, e.g. "take a stroll, hit a trail and fly a kite"; lead-in and activities rotate by date')
a(P,pw,'Even a short outing should feel nice.','Yes/Maybe but no activity fits.')
a(P,pw,'You can head out right now, though conditions aren’t the dreamiest. Keep an eye out for [weak points]. [Activities sentence] [After-window sentence]','Verdict is Maybe and the window starts now.')
a(P,pw,'Hang tight: [day] [time] looks like a lovely time to get outside. Then it will be [summary]. [Activities sentence] [After-window sentence]','Verdict is Maybe with a window later today.')

AF='After-window sentence'
a(AF,'End of the Yes / Maybe paragraph','After [time], [phrases].','A good window is followed by an hour that is ruled out. Shows up to 2 phrases.','')
for ph,wh in [('the light fades','Next hour is dark (see the night variations below)'),('expect [thunderstorms/rain/showers/snow]','Precipitation arrives'),('winds pick up to [N] mph','Wind reaches the limit'),('the chance of precipitation rises to [N]%','Precip chance reaches the limit'),('it drops to [N]°F','Gets too cold'),('it heats up to [N]°F','Gets too hot'),('the ground turns snowy or icy','Ice/snow on the ground'),('air quality worsens (AQI [N])','AQI above the limit'),('it gets humid','Humidity above the limit'),('the ground gets wet','Wet ground'),('conditions turn less ideal','Fallback when none of the above applies')]:
    a(AF,'Phrase used in the After sentence',ph,wh)
a(AF,'Phrase when darkness is the only change','the light fades but it stays [clear / mostly clear / partly cloudy] and [calm / breezy / windy]','Next hour is dark only, with clear or partly cloudy skies.','Calm under 8 mph, breezy under 16, otherwise windy')
a(AF,'Phrase when darkness is the only change','the light fades, with [mostly cloudy / cloudy] skies and [calm / breezy / windy] conditions','Next hour is dark only, cloudy.')
a(AF,'Phrase when darkness is the only change','the light fades, with [rain possible / thunderstorms possible / snow possible / fog]','Next hour is dark only, with that sky.')

N='Night Time paragraph'
nq=['It’s night time and dark out, so most outdoor activities will be challenging unless you have a good headlamp.',
'The sun has called it a day and it’s properly dark out, so outdoor plans will need a flashlight and a good sense of direction.',
'It’s dark out there, which makes most outdoor activities tricky unless you’re carrying a good headlamp.',
'Night has settled in, and with so little light around, trails and open spaces are best saved for daylight.',
'The sun is down, so most outdoor activities will be a challenge unless you’re packing a headlamp and a sense of adventure.',
'Darkness has rolled in, so most outdoor activities will be hard going unless you have a good light with you.']
for s in nq: a(N,pw,s,'Night Time tag, and the place is NOT within about 30 km of a large U.S. city.','Opening sentence: one of six, chosen by the date and the place')
nb=['It’s night time, but a city this size never really goes dark, and plenty of folks are still out and about.',
'It’s late, but the streetlights are glowing and the sidewalks are still lively, so an evening stroll is on the table.',
'The sun is down, but between the city lights and the night owls, the place is still wide awake.',
'It’s dark out, though the city glow makes it easy to see, and there’s usually someone out for a late walk or a bite.',
'Night has fallen and the city is shining. Lit streets and late crowds make it a fine time for a stroll, just stick to well-lit routes.',
'The sky is dark but the skyline isn’t, so with lights and people all around, a short evening outing is easy to enjoy.']
for s in nb: a(N,pw,s,'Night Time tag, and the place is within about 30 km of one of ~65 large U.S. metro centers.','Opening sentence: one of six')
for s in ['It’s [calm/breezy] and [clear/partly cloudy] out there, a nice night for a little stargazing.','With [calm/breezy], [clear/partly cloudy] conditions, the stars should put on a good show.','It’s [calm/breezy] and [clear/partly cloudy], so if you do step out, look up: the night sky is worth a peek.']:
    a(N,pw,s,'Night Time, small town, sky is clear or partly cloudy.','Second sentence: one of three. "calm" under 8 mph, "breezy" otherwise')
for s in ['It’s [calm/breezy] out there, a cozy night to stay in.','It’s [calm/breezy] out there, so settle in with something warm and let the night go by.']:
    a(N,pw,s,'Night Time, small town, cloudy or wet sky.','Second sentence: one of two')
for s in ['It’s [calm/breezy] and [clear/partly cloudy], so the moon and a few of the brightest stars should shine through the city glow.','It’s [calm/breezy] and [clear/partly cloudy] out there, a pleasant night for a late walk under the city lights.']:
    a(N,pw,s,'Night Time, big city, sky is clear or partly cloudy.','Second sentence: one of two')
for s in ['It’s [calm/breezy] out there, a good night for a late bite or a cozy night in.','It’s [calm/breezy] out there, with the clouds soaking up the city glow.']:
    a(N,pw,s,'Night Time, big city, cloudy or wet sky.','Second sentence: one of two')
for s in ['Good news: the sun’s back soon, and [day] [time] looks lovely.','Hang in there, the sun will be back soon, and [day] [time] looks lovely.','Morning is on its way, and [day] [time] looks like a lovely time to head out.']:
    a(N,pw,s,'Night Time and the verdict is Maybe (a window opens later today).','One of three')
for s in ['Your next good window is [day] [time], so sweet dreams until then.','Your next good window is [day] [time], so rest up until then.','Things look good again [day] [time], so get some rest.']:
    a(N,pw,s,'Night Time, small town, verdict is No with a window within 48 hours.','One of three')
for s in ['Your next good window is [day] [time], and the city will be right here waiting.','Your next good window is [day] [time], so enjoy the lights until then.','Things look good again [day] [time].']:
    a(N,pw,s,'Night Time, big city, verdict is No with a window within 48 hours.','One of three')

B='Best Times (empty state)'
bw='Best Times (no window)'
a(B,bw,'You might want to stay inside because [rain / showers / snow / thunderstorms / heavy ...] [is / are] moving through.','No good window in 48 hours and a precipitation type leads (whichever shows up the most hours).','Title; the fireplace scene shows the matching weather in the window')
a(B,bw,'You might want to stay inside because [Calm/Breezy/Windy/Blustery/Howling] wind is moving through.','No window, no precipitation, but wind reaches 25 mph or more.','Title')
a(B,bw,'[Precip] is already in the forecast, / [Precip] moves in around [time],','Precipitation is first.','Followed by:')
a(B,bw,'continuing through the next 48 hours with no clear break in sight. / clearing up by [time].','Precipitation lasts the whole window / ends within it.')
a(B,bw,'Wind picks up too, gusting to [N] mph ([Blustery/Howling/...]) around [time].','Added when there is both precipitation and wind of 25 mph or more.')
a(B,bw,'[Band] wind is already blowing, gusting to [N] mph, / [Band] wind picks up around [time], gusting to [N] mph,','Wind-only case.','Followed by "staying gusty through the next 48 hours." or "calming down by [time]."')
a(B,bw,'Time to stay inside for a while. No good window in the next 48 hours. Rain, wet ground, strong wind or poor air quality are in the way. This updates when the forecast does.','No window and no single clear cause (the fallback).')
a(B,bw,'Your custom Best Times settings may be ruling windows out; use Customize to loosen them or reset to the defaults.','Added when the person has changed the Best Times limits.')
a(B,'Best Times notes','Next 48 hours, daylight only. A maximum of 3 options, ranked by temperature, wind, ground dryness & air quality. Skips rain, icy/snowy ground & darkness. Precip chance is the highest chance of precipitation during the window; humidity is the window average & doesn’t affect the ranking.','Always shown with the list.')
a(B,'Best Times notes','We couldn’t reach the air quality service, so air quality isn’t part of these rankings. Pull down to refresh and try again.','Air-quality data failed to load.')
a(B,'Best Times notes','We couldn’t get recent rainfall data, so ground dryness is estimated from the forecast alone. Pull down to refresh and try again.','Past-rainfall data failed to load.')
a(B,'Best Times notes','You are using custom Best Times settings: [list]. Use Customize to change them or reset to the defaults.','Limits differ from the defaults.')
a(B,'Best Times rows','Day: Today / Tomorrow / [Weekday Month/Day]; Ground: Dry / Damp / Wet; Air: [AQI] · Good / Moderate / Sensitive groups','Every window row.','Up to 3 windows, ranked')

WD='Wind categories'
for lab,r in [('Calm','under 8 mph'),('Breezy','8–15 mph'),('Windy','16–24 mph'),('Blustery','25–33 mph'),('Howling','34 mph and up')]:
    a(WD,'Wind tag in Current Conditions, Wind Today, 7-day outlook, Best Times',lab,r)
a(WD,'Wind sentences (older phrasing)','calm winds / a steady breeze / windy conditions / blustery winds / howling winds','Words for the same five bands where a noun phrase is needed.')

G='Ground conditions'
a(G,'Current Conditions row','Icy — Freezing temps with precipitation','Forecast mentions ice/sleet/freezing rain, or it is 32°F or colder with rain.')
a(G,'Current Conditions row','Snowy — Snow accumulating or expected','Snow in the forecast and 32°F or colder.')
a(G,'Current Conditions row','Wet — Recent or expected precipitation','Rain/showers/drizzle/thunderstorms or snow above freezing.')
a(G,'Current Conditions row','Dry — No precipitation expected','None of the above.')
a(G,'Hero rain/storm outlook','[Rain / Snow] ends in ~[time]  |  [Showers / Thunderstorms / High winds] end in ~[time]  |  [type] [possible] in ~[time]','Precipitation or high wind is active / about to start within 6 hours.','Time rounded to 5 minutes, then hours')

AQ='Air quality and pollen'
for lab,r in [('Good','AQI 0–50'),('Moderate','51–100'),('Unhealthy for Sensitive Groups','101–150'),('Unhealthy','151–200'),('Very Unhealthy','201–300'),('Hazardous','301 and up')]:
    a(AQ,'AQI line + gauge',lab,r)
for lab,r in [('Low','Good'),('Moderate','Moderate'),('High','Unhealthy for Sensitive Groups'),('Very High','Unhealthy'),('Severe','Very Unhealthy'),('Extreme','Hazardous')]:
    a(AQ,'Pollutants (PM2.5) gauge word',lab,f'AirNow category: {r}')
for lab,r in [('None','Estimate is 0'),('Low','Under 20'),('Moderate','20–44'),('High','45–69'),('Very High','70 and up')]:
    a(AQ,'Trees / Weeds / Grasses gauges',lab,r,'')
a(AQ,'Gauge (desktop)','NA','No reading is available for that gauge.','Phone and tablet say "Unavailable"')

E='Error messages'
for s,w in [('We can’t reach the weather services right now. Check your internet connection, then try again.','Network failure.'),
('Something unexpected got in the way. Give it a moment & try again, or search for a different place.','Any other failure.'),
('We couldn’t refresh just now. Pull down to try again in a moment.','Background refresh failed.'),
('We couldn’t look up that place right now. Give it a moment, then try searching again.','Place search failed.'),
('The National Weather Service doesn’t cover this spot. Try a nearby U.S. city or town instead.','Location outside NWS coverage.'),
('The National Weather Service doesn’t have hourly wind data for this area yet. Try a nearby town, or check back soon.','No hourly data for the area.'),
('Your browser can’t share your location. Try searching for a city or ZIP code instead.','Browser has no location support.'),
('We couldn’t get your location. Allow location access for this site in your browser settings, or search for a city instead.','Location permission denied.'),
('Your device couldn’t work out where you are. Try again in a moment, or search for a city or ZIP code.','Location unavailable.'),
('Finding your location is taking too long. Try again, or search for a city or ZIP code.','Location timed out.'),
('We couldn’t find “[search]” in the U.S. Try a city & state, like “Denver, CO”, or a ZIP code.','A search matched no U.S. place.')]:
    a(E,'Error view',s,w)

C='Consent banner'
a(C,'Bottom bar, first visit','Help us count visits? We use Google Analytics to see how many people use Check the Wind and which features they use. It’s for analytics only, with no ads. [What we track]','Shown until the visitor chooses; hides after Accept or Opt Out and is remembered.','Buttons: Opt Out / Accept')

import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','phrasing.csv')
with open(OUT,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Area','Where it appears','Phrase (brackets are filled in)','When it appears','Notes']); w.writerows(R)
print(len(R))
