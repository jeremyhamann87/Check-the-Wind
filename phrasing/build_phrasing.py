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
a(T,tw,'Get outside!','Verdict is Yes: the current hour passes every limit and scores well (score 0.5 or higher), with no Severe/Extreme alert.','Green')
a(T,tw,'Okay for now','Verdict is Maybe and the window starts now: the current hour passes the limits but is not ideal.','Yellow')
a(T,tw,'Wait a bit','Verdict is Maybe and a good window starts later today.','Yellow')
a(T,tw,'Wait a bit','Verdict is No right now but it is passing weather: a good window opens within the next 12 hours (usually tomorrow morning).','Yellow (same tag as the later-today Maybe case)')
a(T,tw,'Stay inside','Verdict is No right now and the next good window is more than 12 hours away (but within [3 / 5 / 7] days).','Orange')
a(T,tw,'Stay in all day','Verdict is No and there is no good window in the next [3 / 5 / 7] days.','Red')
a(T,tw,'Stay aware','It is fine to be out right now (verdict Yes, or Maybe with the window starting now), but rain, snow, storms, strong wind or a rising chance of precipitation arrives within the next 3 hours. No Severe/Extreme alert.','Blue; Use caution and Night time take priority over it')
a(T,tw,'Use caution','A Severe or Extreme National Weather Service alert is active and the verdict is not No (a Yes is downgraded to Maybe).','Orange; takes priority over the other tags unless the verdict is No')
a(T,tw,'Night time','Darkness is the ONLY reason the hour is ruled out, wind is under 16 mph, no Severe/Extreme alert, and the verdict is not Yes.','Purple with a moon')
a('Verdict word','Verdict card (details)','Yes / Maybe / No','Matches the verdict state above.','Also shows the time range (e.g. "from now until 6 PM"); "Right now" when No')

S='One-line summary'
sw='Verdict card, first sentence'
a(S,sw,'[Freezing/Cold/Cool/Mild/Warm/Hot], [calm/breezy/windy/blustery/howling] and dry, with [good/moderate] air quality.','Verdict is Yes (no alert), the ground is dry (wetness under 0.15) and the chance of precipitation in the window is under 10%.','Feel from average temp: under 32 freezing, under 45 cold, under 58 cool, under 72 mild, under 85 warm, otherwise hot. Wind from the top wind in the window (see Wind categories). Air: AQI 50 or less is "good air quality", higher is "moderate air quality"; left out if AQI is unknown.')
a(S,sw,'[Feel] and [wind], with a [N]% chance of [rain / snow / sleet / mixed precip / hail] around [time] and [good/moderate] air quality. / ... with no precipitation expected and ...','Same cases as above, when the ground is damp or wet (0.15 or more) or the chance of precipitation in the window is 10% or more.','Chance is the highest in the window; the time is the hour that chance peaks. "No precipitation expected" when the chance is under 5%. Replaces the old "damp" / "wet" wording.')
a(S,sw,'Okay for now, but not ideal: [weak points].','Verdict is Maybe and the window starts now.','Up to 2 weak points (see Weak points).')
a(S,sw,'Not right now — [reasons]. Later: [the Yes sentence, lowercased]','Verdict is Maybe with a window later today.','Up to 2 reasons (see Reasons a time is ruled out).')
a(S,sw,'Better to skip it for now: [reasons].','Verdict is No.','Up to 2 reasons; a Severe/Extreme alert is listed first as "an active [alert]".')
a(S,sw,'Conditions look fine, but there’s an active [alert]. Be careful.','Severe/Extreme alert and the verdict is Yes or Maybe.','Replaces the lines above')
a(S,'Verdict card, below the sentence','Next best window to get outside: [range].','Verdict is No and a good window exists within [3 / 5 / 7] days.')
a(S,'Verdict card, below the sentence','No good window in the next [3 / 5 / 7] days.','Verdict is No and no window exists.')
a(S,'Verdict card, bottom','Active alert: [event]. Check the details before heading out.','Any active alert that is NOT Severe/Extreme (e.g. an advisory).')

W='Weak points'
for ph,wh in [('wind up to [N] mph','Top wind in the window is 16 mph or more.'),('chilly at [N]°F','Average temp under 40°F.'),('hot at [N]°F','Average temp over 88°F.'),('[N]% chance of [rain / snow / sleet / mixed precip / hail] around [time]','Chance of precipitation is 30% or more; also used instead of "damp ground" when the ground is damp and the chance is 5% or more.'),('damp ground','Ground wetness is 0.15 or more and the chance of precipitation is under 5%.'),('moderate air quality','AQI is above 50.')]:
    a(W,'Okay for now text',ph,wh)

Rs='Reasons a time is ruled out'
for ph,wh,n in [('it’s dark out','No daylight at that hour (uses real sunrise/sunset).',''),
 ('thunderstorms / snow / showers / rain','Forecast shows that precipitation type (not just a "chance of").',''),
 ('wind up to [N] mph','Wind at or above the Best Times wind limit.','Default limit 25 mph'),
 ('[N]% chance of [rain / snow / sleet / mixed precip / hail]','Chance at or above the limit.','Default limit 40%. The type comes from the forecast wording for that hour (hail, mixed / wintry mix, sleet or freezing rain, snow, rain or showers), or from the temperature when the wording only gives a chance: 32°F or colder snow, up to 36°F mixed precip, otherwise rain'),
 ('snowy or icy ground','Ice/snow in the forecast or on the ground.',''),
 ('cold at [N]°F','Below the minimum temperature.','Default 25°F'),
 ('hot at [N]°F','Above the maximum temperature.','Default 100°F'),
 ('poor air quality (AQI [N])','AQI above the limit.','Default limit 150'),
 ('high humidity','Humidity above the limit.','Default 100% (effectively off)'),
 ('wet ground','Ground wetness above the limit (only if the ground setting is on).','Off by default'),
 ('an active [alert]','Severe/Extreme alert is active.','Added to the front of the list')]:
    a(Rs,'Inside the No/Maybe text',ph,wh,n)

A='Activities line'
a(A,'Verdict card under the sentence','Good for [activity, activity or activity].','Yes or Maybe, with at least one activity that fits.','First 3 matching activities (short names)')
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
 ('Dog walks','walk your dog','dog walks','Temp 35–88°F, wind under 25 mph, precip under 40%, AQI 100 or less'),
 ('Bird watching','go bird watching','bird watching','Temp 35–90°F, wind under 15 mph, precip under 20%, AQI 100 or less'),
 ('Mowing the lawn','mow the lawn','mowing','Temp 50–92°F, wind under 20 mph, precip under 10%, ground dry (under 0.15), AQI 100 or less'),
 ('Pruning flowers','prune your flowers','pruning flowers','Temp 40–88°F, wind under 20 mph, precip under 30%, ground under 0.45, AQI 100 or less'),
 ('Washing the car','wash the car','car washing','Temp 50–95°F, wind under 20 mph, precip under 20%, AQI 100 or less'),
 ('Dining al fresco','dine al fresco','dining al fresco','Temp 58–90°F, wind under 12 mph, precip under 15%, AQI 100 or less')]:
    a('Activities','Chip / paragraph',f'{name}  |  short: {short}  |  verb: "{verb}"',cond,'Needs the whole window to fit (lowest/highest temp, top wind, highest precip chance)' if name.startswith('Walking') else '')

P='Paragraph (hero / verdict card)'
pw='Hero paragraph'
a(P,pw,'Conditions look good [from now until 6 PM / today 2 to 6 PM], but there’s an active [alert] for your area. [After-window sentence] Please be careful, and check the alert above before heading outside.','Severe/Extreme alert and verdict is Yes/Maybe.','"Conditions are okay" instead of "look good" when the verdict is the Okay-for-Now kind; "Conditions should be good [day] [time]" when the window is later.')
a(P,pw,'It’s best to stay inside for now: there is an active [alert] and [other reason]. Please stay safe, and check the alert above. Your next best window to get outside is [day time]. / There’s no good outdoor activity window in the next [3 / 5 / 7] days, so it’s a fine time for a movie and a snack.','Severe/Extreme alert and the verdict is No.','Serious tone, no playful wording')
a(P,pw,'[Today / This morning / This afternoon / This evening / Tonight] is a cozy-inside kind of moment: [reasons]. Your next best window to get outside is [day time], so it’s worth the wait. / There’s no good outdoor activity window in the next [3 / 5 / 7] days, so it’s a fine time for a movie and a snack.','Verdict is No, no alert.','')
y1=['[Day] [time] is a lovely time to get outside.','Good news: [day] [time] is a great time to get outside.','Go on, get outside! [Day] [time] looks lovely.']
for s in y1: a(P,pw,s,'Verdict is Yes and it is comfortable (average 50–86°F, ground not wet).','One of three, chosen by the date')
for s in ['[Day] [time] is a good time to get outside.','Good news: [day] [time] works for getting outside.']: a(P,pw,s,'Verdict is Yes but not especially comfortable.','One of two, chosen by the date')
a(P,pw,'Stay aware: after [time], [what is coming].','Stay aware tag: weather arrives within 3 hours.','Replaces the plain "After [time]…" sentence')
for s in ['[Today / This morning / This afternoon / This evening / Tonight] will be [the summary sentence, lowercased]','Expect [the summary sentence, lowercased]']: a(P,pw,s,'Verdict is Yes (second sentence).','One of two. The time word comes from the clock where the place is: 5 AM to noon “This morning”, noon to 5 PM “This afternoon”, 5 to 9 PM “This evening”, otherwise “Tonight”. “Today” when the good window starts now (before noon) and runs to 5 PM or later.')
for s in ['This is great weather to [activities].','It’s a lovely time to [activities].','You could [activities].','Perfect conditions to [activities].']: a(P,pw,s,'Yes/Maybe with at least one fitting activity.','Up to 3 activity verbs, e.g. "take a stroll, hit a trail or fly a kite"; lead-in and activities rotate by date')
a(P,pw,'Even a short outing should feel nice.','Yes/Maybe but no activity fits.')
W5='Work week (Monday to Friday)'
ww='Hero text, replaces the activities sentence'
a(W5,ww,'The morning commute and school drop-off look smooth, with dry roads and light winds[ for the walk to [subway / light rail / streetcar]].','Before 9 AM on a weekday, with nothing in the 6–9 AM window ruling it out. “and school drop-off” is left out June to August; “looks” when only the commute is named.','Big cities add the walk to the named transit (not for “a bus”). Dry roads need wetness under 0.15 and precipitation under 15%, otherwise “little to slow you down”. “just a breeze” instead of “light winds” when the wind reaches 12 mph.')
a(W5,ww,'School pick-up and the drive home look easy, with dry roads and light winds.','12 PM to 4 PM on a weekday from September to May, with nothing ruling out the 2–4 PM pick-up window or the drive home.','Pick-up uses 2–4 PM (or now to 4 PM once it is 3 PM); the drive home uses 4–6 PM')
a(W5,ww,'The drive home looks easy, with dry roads and light winds around [time]. / Expect dry roads and light winds for the drive home around [time].','9 AM to 6 PM on a weekday (and in the afternoon outside the school months). The time is the middle of the 4–6 PM window, or of the next 3 hours from 3 PM.','One of two, chosen by the date')
a(W5,ww,'After work, you could [activities]. / Once you clock out, it’s a nice time to [activities]. / After work is a good time to [activities].','Follows the drive-home sentence on a weekday from 9 AM to 6 PM when at least one activity fits the daylight hours between 5 and 8 PM.','Up to 3 activity verbs from the same list as the weekend sentence; one of three lead-ins, chosen by the date')
a(W5,ww,'After work it will be [feel] at [temp], perfect for a walk to unwind. / It should be [feel] after work, a good time to decompress with a stroll.','Used instead of the activities when none fit but the afternoon is 45–88°F, precipitation under 20% and wind under 16 mph.','One of two, chosen by the date')
a(W5,ww,'It’s a nice day to take your lunch break outside. / Take your lunch outside if you can.','11 AM to 2 PM on a weekday when the current hour is dry (under 20%), under 16 mph and 50–88°F.','Comes before the commute sentence')
a(W5,ww,'It’s a good evening to unwind after work. / A fine evening to decompress after a long day.','6 PM or later on a weekday (still light), 45–88°F, precipitation under 20% and wind under 16 mph.','One of two, chosen by the date; nothing is added when it is not comfortable')
a(W5,ww,'Give yourself a little extra time for [the morning commute and school drop-off / school pick-up / the drive home]: expect [issues]. / Plan on a slower run for [the same], with [issues].','A weekday window has trouble: 40% or more chance of precipitation, icy roads, fog, wind of 22 mph or more, heat over 92°F or temperatures under 28°F. Up to 2 issues; names every window with trouble.','Also added to the “cozy-inside” paragraph on a weekday when the verdict is No (no alert)')
HD='US federal holidays'
hw='Hero text, first sentence'
hwhen='On the day itself, for places in the U.S. (not Canada), unless there is a Severe/Extreme alert, a tornado or flash flood warning, or it is the small hours before dawn.'
for ph,wh in [('Happy New Year!','January 1'),('Happy Martin Luther King Jr. Day!','Third Monday of January'),('Happy Presidents’ Day!','Third Monday of February'),('Take a moment to remember those who served this Memorial Day.','Last Monday of May'),('Happy Juneteenth!','June 19'),('Happy Fourth of July!','July 4'),('Happy Labor Day!','First Monday of September'),('Happy Indigenous Peoples’ Day!','Second Monday of October'),('Thank you to everyone who has served this Veterans Day.','November 11'),('Happy Thanksgiving!','Fourth Thursday of November'),('Merry Christmas!','December 25')]:
    a(HD,hw,ph,wh+'. '+hwhen,'')
a(HD,hw,'[Holiday] is observed today.','The Friday before (holiday on a Saturday) or the Monday after (holiday on a Sunday) a fixed-date holiday: New Year’s Day, Juneteenth, Fourth of July, Veterans Day, Christmas.','Dec 31 when January 1 is a Saturday')
a(HD,hw,'The forecast looks good for fireworks tonight. / A [N]% chance of [rain / …] around [time] could interrupt tonight’s fireworks.','July 4 itself, until 10 PM. Looks at 8–10 PM: a 30% or higher chance of precipitation gives the second sentence; otherwise wind under 20 mph gives the first.','Nothing is added when it is windier than that')
a(HD,hw,'(the work-week sentences are not used)','Any federal holiday, so a weekday holiday gets the weekend-style activity ideas instead of commute and school wording.','')
a(P,pw,'You can head out right now, though conditions aren’t the dreamiest. Keep an eye out for [weak points]. [Activities sentence] [After-window sentence]','Verdict is Maybe and the window starts now.')
a(P,pw,'[[Today / This morning / This afternoon / This evening / Tonight]], [why it is not good right now], so hang tight: [day] [time] looks like a lovely time to get outside. Then it will be [summary]. [Activities sentence] [After-window sentence]','Verdict is Maybe with a window later today.','Up to two reasons, e.g. "Winds up to 33 mph right now, so hang tight: today from 5 to 7 PM looks like a lovely time…"')
for ph,wh in [('it’s dark out','No daylight right now.'),('winds up to [N] mph','Wind at or above the limit.'),('a [N]% chance of [rain / snow / sleet / mixed precip / hail]','Chance of precipitation at or above the limit.'),('it’s raining / it’s snowing / there are showers around / there are thunderstorms around','Precipitation in the forecast right now.'),('the ground is snowy or icy','Ice or snow on the ground.'),('the ground is wet','Wet ground (when that setting is on).'),('it’s cold at [temp] / it’s hot at [temp]','Outside the temperature limits.'),('air quality is poor (AQI [N])','AQI above the limit.'),('it’s humid','Humidity above the limit.')]:
    a(P,pw,ph,wh + ' Used in the "so hang tight" line.','')

AF='After-window sentence'
a(AF,'End of the hero text','After [time], [phrases]. / After the sun sets at [exact sunset time, e.g. 6:29 PM], [phrases].','A good window is followed by an hour that is ruled out. Shows up to 2 phrases. The sunset version is used when the light fading comes first.','Any sentence about the sun setting is moved to the very end of the hero text, after the clothing sentence. The “After [time]” version stays in place.')
a(AF,'End of the hero text','The sun sets at [exact sunset time].','Added at the end when the text has not already said when the sun sets and the sun is still to set today (not at night, not under a severe alert).','Last sentence of the hero text, after the clothing sentence')
for ph,wh in [('the light fades','Next hour is dark (see the night variations below)'),('expect [thunderstorms/rain/showers/snow]','Precipitation arrives'),('winds pick up to [N] mph','Wind reaches the limit'),('the chance of [rain / snow / sleet / mixed precip / hail] rises to [N]%','Precip chance reaches the limit'),('it drops to [N]°F','Gets too cold'),('it heats up to [N]°F','Gets too hot'),('the ground turns snowy or icy','Ice/snow on the ground'),('air quality worsens (AQI [N])','AQI above the limit'),('it gets humid','Humidity above the limit'),('the ground gets wet','Wet ground'),('conditions turn less ideal','Fallback when none of the above applies')]:
    a(AF,'Phrase used in the After sentence',ph,wh)
a(AF,'Phrase when darkness is the only change','the light fades but it stays [clear / mostly clear / partly cloudy] and [calm / breezy / windy]','Next hour is dark only, with clear or partly cloudy skies.','Calm under 8 mph, breezy under 16, otherwise windy')
a(AF,'Phrase when darkness is the only change','the light fades, with [mostly cloudy / cloudy] skies and [calm / breezy / windy] conditions','Next hour is dark only, cloudy.')
a(AF,'Phrase when darkness is the only change','the light fades, with [rain possible / thunderstorms possible / snow possible / fog]','Next hour is dark only, with that sky.')

N='Night time paragraph'
nq=['[Today / This morning / This afternoon / This evening / Tonight] is dark, so most outdoor activities will be challenging unless you have a good headlamp.',
'The sun has called it a day and it’s properly dark out, so outdoor plans will need a flashlight and a good sense of direction.',
'[Today / This morning / This afternoon / This evening / Tonight] is dark, which makes most outdoor activities tricky unless you’re carrying a good headlamp.',
'Night has settled in, and with so little light around, trails and open spaces are best saved for daylight.',
'The sun is down, so most outdoor activities will be a challenge unless you’re packing a headlamp and a sense of adventure.',
'Darkness has rolled in, so most outdoor activities will be hard going unless you have a good light with you.']
for s in nq: a(N,pw,s,'Night time tag, and the place is NOT within about 30 km of a large U.S. or Canadian city.','Opening sentence: one of six, chosen by the date and the place')
nb=['[Today / This morning / This afternoon / This evening / Tonight], a city this size never really goes dark, and plenty of folks are still out and about.',
'[Today / This morning / This afternoon / This evening / Tonight], the streetlights are glowing and the sidewalks are still lively, so an evening stroll is on the table.',
'The sun is down, but between the city lights and the night owls, the place is still wide awake.',
'[Today / This morning / This afternoon / This evening / Tonight] is dark, though the city glow makes it easy to see, and there’s usually someone out for a late walk or a bite.',
'Night has fallen and the city is shining. Lit streets and late crowds make it a fine time for a stroll, just stick to well-lit routes.',
'The sky is dark but the skyline isn’t, so with lights and people all around, a short evening outing is easy to enjoy.']
for s in nb: a(N,pw,s,'Night time tag, and the place is within about 30 km of one of ~75 large U.S. and Canadian city centers.','Opening sentence: one of six')
for s in ['It’s [calm/breezy] and [clear/partly cloudy] out there, a nice night for a little stargazing.','With [calm/breezy], [clear/partly cloudy] conditions, the stars should put on a good show.','It’s [calm/breezy] and [clear/partly cloudy], so if you do step out, look up: the night sky is worth a peek.']:
    a(N,pw,s,'Night time, small town, sky is clear or partly cloudy.','Second sentence: one of three. "calm" under 8 mph, "breezy" otherwise')
for s in ['It’s [calm/breezy] out there, a cozy night to stay in.','It’s [calm/breezy] out there, so settle in with something warm and let the night go by.']:
    a(N,pw,s,'Night time, small town, cloudy or wet sky.','Second sentence: one of two')
for s in ['It’s [calm/breezy] and [clear/partly cloudy], so the moon and a few of the brightest stars should shine through the city glow.','It’s [calm/breezy] and [clear/partly cloudy] out there, a pleasant night for a late walk under the city lights.']:
    a(N,pw,s,'Night time, big city, sky is clear or partly cloudy.','Second sentence: one of two')
for s in ['It’s [calm/breezy] out there, a good night for a late bite or a cozy night in.','It’s [calm/breezy] out there, with the clouds soaking up the city glow.']:
    a(N,pw,s,'Night time, big city, cloudy or wet sky.','Second sentence: one of two')
for s in ['Good news: the sun’s back soon, and [day] [time] looks lovely.','Hang in there, the sun will be back soon, and [day] [time] looks lovely.','Morning is on its way, and [day] [time] looks like a lovely time to head out.']:
    a(N,pw,s,'Night time and the verdict is Maybe (a window opens later today).','One of three')
for s in ['Your next best window to get outside is [day] [time], so sweet dreams until then.','Your next best window to get outside is [day] [time], so rest up until then.','Things look good again [day] [time], so get some rest.']:
    a(N,pw,s,'Night time, small town, verdict is No with a window within [3 / 5 / 7] days.','One of three')
for s in ['Your next best window to get outside is [day] [time], and the city will be right here waiting.','Your next best window to get outside is [day] [time], so enjoy the lights until then.','Things look good again [day] [time].']:
    a(N,pw,s,'Night time, big city, verdict is No with a window within [3 / 5 / 7] days.','One of three')

B='Best Times (empty state)'
bw='Best Times (no window)'
a(B,bw,'You might want to stay inside because [rain / showers / snow / thunderstorms / heavy ...] [is / are] moving through.','No good window in [3 / 5 / 7] days and a precipitation type leads (whichever shows up the most hours).','Title; the fireplace scene shows the matching weather in the window')
a(B,bw,'You might want to stay inside because [Calm/Breezy/Windy/Blustery/Howling] wind is moving through.','No window, no precipitation, but wind reaches 25 mph or more.','Title')
a(B,bw,'[Precip] is already in the forecast, / [Precip] moves in around [time],','Precipitation is first.','Followed by:')
a(B,bw,'continuing through the next [3 / 5 / 7] days with no clear break in sight. / clearing up by [time].','Precipitation lasts the whole window / ends within it.')
a(B,bw,'Wind picks up too, gusting to [N] mph ([Blustery/Howling/...]) around [time].','Added when there is both precipitation and wind of 25 mph or more.')
a(B,bw,'[Band] wind is already blowing, gusting to [N] mph, / [Band] wind picks up around [time], gusting to [N] mph,','Wind-only case.','Followed by "staying gusty through the next [3 / 5 / 7] days." or "calming down by [time]."')
a(B,bw,'Time to stay inside for a while. No good window in the next [3 / 5 / 7] days. Rain, wet ground, strong wind or poor air quality are in the way. This updates when the forecast does.','No window and no single clear cause (the fallback).')
a(B,bw,'Your custom Best Times settings may be ruling windows out; use Customize to loosen them or reset to the defaults.','Added when the person has changed the Best Times limits.')
a(B,'Best Times: Customize dialog, How Best Times work','Top 3: the next [3 / 5 / 7] days, daylight only. Up to 3 options across those days, ranked by temperature, wind, ground dryness & air quality. Skips rain, icy/snowy ground & darkness. Precip chance is the highest chance of precipitation during the window; humidity is the window average.','Shown at the bottom of the Customize dialog when the Best Times view is Top 3 (there is no longer an info button on the card).')
a(B,'Best Times: Customize dialog, How Best Times work','7-Day: the best window of each of the next 7 days, daylight only, chosen by temperature, wind, ground dryness & air quality. A day with nothing suitable says why. Skips rain, icy/snowy ground & darkness. Precip chance is the highest chance of precipitation during the window; humidity is the window average.','Shown at the bottom of the Customize dialog when the Best Times view is 7-Day (the default).')
a(B,'Best Times view selector','7-Day | Top 3 (a light two-label control in the module header, to the left of the Customize button; the chosen label has a thin rounded outline and medium-weight text; the other is regular weight; the text and the outline are the same gray-blue as the module title)','Always shown in the header. 7-Day is the default; the choice is remembered on that device.','7-Day: one card per day for the next 7 days. Top 3: the three best windows overall, ranked with medals.')
a(B,'Best Times cards (7-Day view)','Card header: [Today / weekday name] [time range of that day’s best window]; below it the temperature range, sky icon and the summary sentence','One card per day for up to 7 days; a day with no daylight left is skipped.','The header is tinted by that window’s top wind (Calm, Breezy, Windy…); no medals. Tapping a card opens the same details as Top 3.')
a(B,'Best Times cards (7-Day view)','[Weekday] No good window / Skipped: [up to 2 reasons: strong winds, rain likely, snow likely, thunderstorms likely, snowy or icy ground, cold temperatures, heat, poor air quality, high humidity, wet ground] / No stretch of good weather is long enough to plan around.','A day in the 7-Day view where no window passes your limits (or every window is under 2 hours).','The reasons are the most common ones across that day’s daylight hours. These cards are not tappable.')
a(B,'Time frame help (Customize dialog)','How many days ahead Top 3 looks. The 7-Day view always covers seven.','Always, under the Time frame control.','')
a(B,'Best Times: Customize dialog, How Best Times work','We couldn’t reach the air quality service, so air quality isn’t part of these rankings. Pull down to refresh and try again.','Air-quality data failed to load.')
a(B,'Best Times: Customize dialog, How Best Times work','We couldn’t get recent rainfall data, so ground dryness is estimated from the forecast alone. Pull down to refresh and try again.','Past-rainfall data failed to load.')
a(B,'Best Times cards: wind tag','[Calm / Breezy / Windy / Blustery / Howling] (a small colored tag to the right of the sky icon, same colors as the 7-Day Outlook)','Every card that has a window, in both 7-Day and Top 3.','Based on the strongest wind in the window: under 8 mph Calm, 8–15 Breezy, 16–24 Windy, 25–33 Blustery, 34+ Howling')
a(B,'Best Times cards','Card header: [medal] [Today / weekday name, e.g. Sunday] [time range, e.g. 7 AM–6 PM or Now–6 PM], above a divider','Every card.','Up to 3 cards, ranked 1 to 3 with gold, silver and bronze medals; on phones they scroll sideways')
a(B,'Best Times cards','[low–high]°F (large) with the sky icon for the middle hour of the window','Every card.','Metric (°C) in Canada')
a(B,'Best Times cards','Same sentence as the verdict card’s Yes line, built from the window: [Feel], [wind] and dry, with [air quality] / [Feel] and [wind], with a [N]% chance of precipitation around [time] and [air quality]','Every card.','See the One-line summary rows for the thresholds')
a(B,'Best Times cards','(No visible label) Tapping or clicking a card opens its detail dialog; screen readers hear “[Day] [time], show details”','Every card.','A small arrow at the right of the card header hints that the card opens')
a(B,'Best Times detail dialog','Title: [Day] · [time range]; the place name; the summary sentence','Card detail dialog.')
a(B,'Best Times detail dialog','Temperature: [low–high] across the window | Sky: [forecasts in the window] | Wind: [low–high] · [Calm…Howling], from the [direction] | Chance of [rain / snow / sleet / mixed precip / hail]: Up to [N]% | Ground: [Dry/Damp/Wet] | Humidity: [low–high], average [N]% | Air quality: AQI up to [N] · [Good air…]','Card detail dialog, top list.','NA when a value is not available')
a(B,'Best Times detail dialog','Hour by hour: Hour | Temp | Sky | Wind | Precip | Humidity | AQI | Ground','Card detail dialog, table with one row per hour in the window.','NA when a value is not available')
a(B,'Best Times: Customize dialog','Time frame: 3 days / 5 days / 7 days (segmented control, first in the dialog; default 5 days). Highest temperature is the first slider, then Lowest temperature.','Always.','Sets how far ahead Best Times looks; the day counts in the explainer and the no-window messages follow it')
a('Current conditions (right now)','Hero sky line and icon','Thunderstorms / Heavy rain / Rain / Light rain / Heavy snow / Snow / Light snow','Radar at the place, the nearest weather station observation (under 90 minutes old) or the Open-Meteo model sees precipitation. Radar: intense (orange, red, purple) echoes mean thunderstorms, yellow heavy, green moderate, blue light; lighter echoes need another source or a 30%+ chance to count.','Replaces the forecast wording (which can say "Patchy Fog" while it is storming). Snow when the station says snow or it is 33°F or colder.')
a('Current conditions (right now)','Hero sky line','[Station\'s own wording, e.g. Cloudy / Clear / Fog/Mist]','Nothing is falling and a station observation is under 90 minutes old.','Falls back to the forecast wording when there is no recent observation')
a('Current conditions (right now)','Hero sky line','Rain Likely / Snow Likely','No observation, and the forecast wording has no precipitation but the chance is 70% or more.','Also applied to later hours with a 60%+ chance whose wording leads with fog or cloud')
a('Current conditions (right now)','Hero temperature and wind','[Station temperature] and [station wind speed and direction] for the current hour','A station observation under 90 minutes old.','Otherwise the forecast for the hour')
a('Alerts in the hero text','Hero text (first sentences)','A wind advisory is in effect until 11 PM. / A wind advisory takes effect at 7 AM and runs until 11 PM. / An excessive heat warning is in effect until 8 PM Wed.','Every alert in the banner except a tornado warning and the one the text is already built around (a severe warning, or a flash flood warning). Times are in the place’s time zone; today is left off, then “tomorrow” or the weekday.','Wind alerts add “Winds could reach [N] mph.” (the top wind in the next 12 hours, when it is 15 mph or more). At most two alerts, then “Plus N more alert(s), listed above.”')
a('Within an hour of sunrise','Hero headline','Good morning. Your next best window to get outside is [range].','Calm night (Night time tag) with sunrise less than 60 minutes away.','')
a('Within an hour of sunrise','Hero text','The town is waking up: birds are chirping, people are getting ready, and coffee is brewing. / Dawn is close: birds are chirping, the town is stirring, and coffee is brewing in kitchens everywhere. / The town is slowly waking up, with birds chirping, people getting ready and coffee brewing.  +  The sun rises at [time].','Same. One of three, chosen by the date.','Weather at that hour: “[reasons], so stay snuggled up in bed.” + “The town is waking up and people are getting ready, so stay safe at home until it passes.” Other states (not under an alert): “The town is waking up, with birds chirping, people getting ready and coffee brewing.” before the sunrise time.')
a('Sunrise','Hero text (last sentence of the detail)','The sun rises at [exact sunrise time, e.g. 6:24 AM].','Within the 90 minutes before sunrise, in any state except a tornado warning.','Not repeated if the text already says it')
a('What to wear','Hero text, gray line and card advice','Light, breathable clothes will feel best. / Dress light in breathable clothes, and bring water. (no sunscreen or hat)','It is dark right now (night, or before sunrise) and it is not raining.','The sun wording (sunscreen, hat) only appears in daylight')
a('What to wear','Hero text, gray line and card advice','Light, quick-drying clothes will feel best. Pack an umbrella and a rain coat if you’re headed out. / Rain is on the way, so pack an umbrella and a rain coat if you’re headed out.','Rain, thunderstorms or a 60%+ chance of precipitation in the next 7 hours (the sun wording, sunscreen and hat, is dropped).','Short list: light clothes, umbrella, rain coat')
a('Tornado warning','Hero headline','Tornado warning in effect: take shelter now.','A Tornado Warning or Tornado Emergency is active at the place.','Overrides the verdict (always a No) and every other wording')
a('Tornado warning','Hero text','Take shelter now: get to the lowest level of the building you’re in, and into the innermost room, away from windows. Tune in to your local weather for the most up-to-date information.','Same.','Only these two sentences: no activities, clothing or pet tips')
a('Flash flood warning','Hero headline','Flash flood warning in effect: turn around, don’t drown.','A Flash Flood Warning or Flash Flood Emergency is active at the place (and no tornado warning).','Verdict otherwise as normal, but never better than Okay (Use caution)')
a('Flash flood warning','Hero text (first sentence)','Never drive through flooded roadways or around barricades. Turn around, don’t drown.','Same.','Followed by the usual text; clothing and pet tips are left out under any severe alert')
a('Alert banner colors','Alert banners, list dots and hover previews (no wording)','Tornado, hurricane and other warnings: red. Flash flood warning / emergency: lime green. Severe thunderstorm warning: yellow. Every watch: blue. Advisories: slate blue.','Matches the alert event name.','')
a('Tornado warning','Tag','Take shelter (red)','Same.','')
a('Radar warnings','Expanded radar (outlines only, no key or switch)','Tap an outline: [warning name], Until [time], Issued by NWS [office], [Tornado / Wind up to N mph / Hail up to N in tags], Details link','Active tornado, severe thunderstorm, flash flood, flood and special marine warning polygons (U.S. only).','Colors: tornado red, severe thunderstorm orange, flash flood lime green, flood darker green, special marine dark orange; each with a thin black edge. Refreshes every 3 minutes.')
a('Radar warnings','Radar in Current Conditions (outline only)','Warning outlines in the same colors, no key','Active warning polygons near the place (U.S. only).','')
a('Page layout','Phones and tablets (no wording)','Hero text, then Current Conditions, then the radar, then Best Times to Get Outside. On tablets Current Conditions and the radar sit side by side. Desktop is unchanged.','Always.','There is no separate layout for warnings any more')
a('After midnight, before sunrise','Hero headline','Time to sleep. Your next best window to get outside is [range].','Calm night (Night time tag), after midnight and before sunrise.','')
a('After midnight, before sunrise','Hero text','[Today / This morning / This afternoon / This evening / Tonight] is quiet and still, so it’s the perfect time to stay snuggled up in bed. / Everything is still and dark outside, so stay cozy under the covers. / The whole town is asleep, so stay tucked in, warm and snug.  +  Rest up and stay safe at home until the sun comes up. / Sleep tight, and keep the adventures for the morning. / Stay cozy and safe at home until daylight.','Same. One of each, chosen by the date. No clothing line.','Weather at night: “[reasons, e.g. There are thunderstorms around], so stay snuggled up in bed.” + “Stay safe and warm at home until it passes. / Be safe at home, and let the night pass by.”')
a('After midnight, before sunrise','Hero text, when the weather is also rough','[Tonight / This morning], [up to 2 reasons, e.g. it’s raining and winds up to 30 mph], so stay snuggled up in bed. / [Tonight / This morning] is a rough one out there, so stay snuggled up in bed.','Verdict is No before dawn (not the calm-night case above) and there is no Severe/Extreme alert.','The first form lists the reasons; the second is used when there are none')
a('Search','Search box (Enter on a street address)','Street addresses like “123 Main St, Denver, CO” are found on submit and the weather is for that address’s coordinates; the place name shown is the nearest town','The text starts with a house number and a street name (U.S. and Canada). ZIP codes and place names use the usual place search.','Not looked up while typing')
a(B,'Best Times few windows','There is only 1 best time right now. Adjust settings to see more. / There are only 2 best times right now. Adjust settings to see more.','Under the cards when only 1 or 2 windows are found (light gray text).','Not shown with 3 windows or with none (the empty state takes over)')
a(B,'Link preview image','Check the Wind logo windmill with "Check the Wind", "The friendly outdoor planner: wind, weather and the best times to get outside" and checkthewind.com (og-image.png, 1200 x 630)','When the site link is shared in Messages, WhatsApp, Slack, Facebook, X and similar.','Same image for every place; the page title and description come from the meta tags')

WD='Wind categories'
for lab,r in [('Calm','under 8 mph'),('Breezy','8–15 mph'),('Windy','16–24 mph'),('Blustery','25–33 mph'),('Howling','34 mph and up')]:
    a(WD,'Wind tag in Current Conditions, Wind Today, 7-day outlook, Best Times',lab,r)
a(WD,'Wind sentences (older phrasing)','calm winds / a steady breeze / windy conditions / blustery winds / howling winds','Words for the same five bands where a noun phrase is needed.')

G='Ground conditions'
a(G,'Current Conditions row','Icy — Freezing temps with [rain / sleet / mixed precip]','Forecast mentions ice/sleet/freezing rain, or it is 32°F or colder with rain.')
a(G,'Current Conditions row','Snowy — Snow accumulating or expected','Snow in the forecast and 32°F or colder.')
a(G,'Current Conditions row','Wet — Recent or expected [rain / snow / mixed precip]','Rain/showers/drizzle/thunderstorms or snow above freezing.')
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
('We don’t have weather data for this spot yet. Try a nearby U.S. or Canadian city or town instead.','Location outside U.S. and Canadian coverage.'),
('The National Weather Service doesn’t have hourly wind data for this area yet. Try a nearby town, or check back soon.','No hourly data for the area.'),
('Your browser can’t share your location. Try searching for a city or ZIP code instead.','Browser has no location support.'),
('We couldn’t get your location. Allow location access for this site in your browser settings, or search for a city instead.','Location permission denied.'),
('Your device couldn’t work out where you are. Try again in a moment, or search for a city or ZIP code.','Location unavailable.'),
('Finding your location is taking too long. Try again, or search for a city or ZIP code.','Location timed out.'),
('We couldn’t find “[search]” in the U.S. or Canada. Try a street address, a city & state or province, like “Denver, CO” or “Toronto, ON”, or a ZIP code.','A search matched no U.S. or Canadian place.')]:
    a(E,'Error view',s,w)

a('Units','Every temperature and wind speed shown','°C and km/h for visitors in Canada and for anyone viewing a Canadian place; °F and mph everywhere else','The browser reports a Canadian time zone (Toronto, Vancouver, Halifax, etc.) or a Canadian language (en-CA, fr-CA), OR the place being viewed is in Canada.','Wind categories in km/h: Calm 0–12, Breezy 13–25, Windy 26–39, Blustery 40–54, Howling 55+')
HL='Headline (bold, top of the hero)'
hw='Bold headline under the city name; the tag sits beside the city. Each sentence is on its own line.'
for ph,wh,n in [
 ('Lovely through the evening. / Lovely until [rain arrives / storms arrive / the wind picks up / ...] around [time]. / Lovely [day] [time range].','Verdict Yes and comfortable (average 50–86°F, ground not wet). "Through the evening" when only the sun going down ends the window; the weather wording when something else does.','Canadian: "Beauty day, eh? Nice out until [time]." / "Give’r! Lovely until [time]."'),
 ('Nice out through the evening. / Nice out until [weather] around [time]. / Nice out [day] [time range].','Verdict Yes, not especially comfortable. Same "through the evening" and weather rules as above.','Canadian: "Not bad, eh. Nice out until [time]."'),
 ('Nice out until [time], then [rain / snow / storms / wind / ice].','Stay aware: weather arrives within 3 hours.',''),
 ('Doable, not ideal: [first weak point]. / Doable now, but [weather] by [time].','Verdict Maybe and the window starts now.',''),
 ('[Why short] now. Lovely [day] [time range].','Verdict Maybe with a window later today (why: Dark out, Storms, Rain, Snow, Showers, Windy, Rain likely, Icy ground, Cold, Hot, Poor air, Humid, Wet ground).','Canadian: "Lovely, eh: …"'),
 ('[Why short]. Next best window to get outside: [day] [time range].','Verdict No (no alert), a good window within [3 / 5 / 7] days.',''),
 ('[Why short]. No good window for [3 / 5 / 7] days.','Verdict No, no window in [3 / 5 / 7] days.',''),
 ('Dark out. Next best window to get outside: [day] [time range]. / Dark out. Not a night for outdoor plans.','Night time tag.','Canadian: "Dark out, eh."'),
 ('Fine out, but there’s an active [alert].','Severe/Extreme alert and the verdict is Yes or Maybe.',''),
 ('[Alert] in effect.','Severe/Extreme alert and the verdict is No (e.g. "Hurricane warning in effect.").','')]:
    a(HL,hw,ph,wh,n)
a(HL,'Gray text under the headline','The earlier paragraph’s sentences (conditions, ideas, after-window, "hang tight" reasons, clothing, transit, pets) minus the sentence the headline already says. One paragraph.','Every state. A severe alert shows its safety sentence only (no clothing or pet tips).','The headline never repeats the wording of the tag (Get outside!, Okay for now, Wait a bit, Stay aware, Stay inside, Stay in all day, Use caution, Night time).')
a(HL,'Gray text under the headline','Bring a jacket or a warm sweater, plus an umbrella or a rain jacket.','Cool and rain.','Two "Bring…" sentences are merged into one')

BC='Big cities'
bcw='Hero paragraph and details (cities of roughly the top ~75 U.S./Canadian metros)'
bc_cond='The place is within about 30 km of a large U.S. or Canadian city centre.'
for name,verb,short,cond in [
 ('City walks','wander the neighborhoods on foot','city walks','Temp 28–95°F, wind under 25 mph, precip under 40%, AQI 100 or less'),
 ('Park time','spend time in the park','park time','Temp 45–90°F, wind under 20 mph, precip under 30%, AQI 100 or less'),
 ('Sidewalk cafés & patios','grab a table on a patio','patio dining','Temp 58–90°F, wind under 14 mph, precip under 15%, AQI 100 or less'),
 ('Rooftop bars','have a drink at a rooftop bar','rooftop bars','Temp 62–92°F, wind under 12 mph, precip under 15%, AQI 100 or less'),
 ('Outdoor concerts','catch a concert outdoors','outdoor concerts','Temp 55–90°F, wind under 15 mph, precip under 10%, AQI 100 or less'),
 ('Museums & theaters','visit a museum or catch a show','museums and shows','Temp 15–100°F, wind under 30 mph, precip under 60%, AQI 150 or less'),
 ('Dinner out','head out to dinner at a favorite restaurant','dinner out','Temp 20–100°F, wind under 30 mph, precip under 50%, AQI 150 or less'),
 ('Street markets','browse a street market','street markets','Temp 45–90°F, wind under 18 mph, precip under 20%, AQI 100 or less'),
 ('Cycling','cruise the bike lanes','cycling','Temp 40–90°F, wind under 15 mph, precip under 20%, ground dry, AQI 100 or less'),
 ('Running','go for a run','running','Temp 28–78°F, wind under 20 mph, precip under 30%, AQI 100 or less'),
 ('Dog walks','walk your dog','dog walks','Temp 35–88°F, wind under 25 mph, precip under 40%, AQI 100 or less')]:
    a(BC,'Chip / paragraph (big cities use this list instead of the general Activities list)',f'{name}  |  short: {short}  |  verb: "{verb}"',bc_cond + ' ' + cond,'')
a(BC,'Activities line','Better saved for museums, shows and a good restaurant.','Big city and the verdict is No.','Other places say "Better saved for indoor plans."')
a(BC,'Verdict details','A good time for a museum, a show or a long dinner.','Big city and the verdict is No.','Other places say "A good time for indoor plans."')
a(BC,bcw,'There’s no good outdoor activity window in the next [3 / 5 / 7] days, so it’s a fine time for a museum, a show or a long dinner out.','Big city, verdict No, no window in [3 / 5 / 7] days, no alert.','')

for city,tr in [('New York','the subway'),('Los Angeles','the Metro'),('Chicago','the L'),('Houston','the light rail'),('Phoenix','the light rail'),('Philadelphia','the subway'),('San Diego','the trolley'),('Dallas','the light rail'),('San Jose','the light rail'),('Charlotte','the light rail'),('San Francisco','BART or Muni'),('Seattle','the light rail (Link; Seattle has no subway)'),('Denver','the light rail'),('Washington, DC','the Metro'),('Boston','the T'),('Baltimore','the Metro'),('Tucson','the streetcar'),('Sacramento','the light rail'),('Atlanta','MARTA'),('Kansas City','the streetcar'),('Miami','Metrorail'),('Oakland','BART'),('Minneapolis','the light rail'),('Cleveland','the rapid transit'),('New Orleans','the streetcar'),('Pittsburgh','the light rail'),('Cincinnati','the streetcar'),('St. Louis','the light rail'),('Salt Lake City','the light rail'),('Portland','the light rail'),('Norfolk','the light rail'),('Buffalo','the Metro Rail'),('Toronto','the subway'),('Montreal','the Metro'),('Vancouver','the SkyTrain'),('Calgary','the CTrain'),('Edmonton','the LRT'),('Ottawa','the O-Train')]:
    a('Big city transit','Used in the "or a cab beats a long walk" line',city + ': ' + tr,'Big city with rain, snow, bitter cold or strong wind.','Checked against Wikipedia lists of U.S. heavy rail and light rail systems')
a('Big city transit','Used in the "or a cab beats a long walk" line','All other big cities: a bus','Big city with rain, snow, bitter cold or strong wind.','No rail system, or only a limited one')

WR='What to wear and pets'
wrw='Last sentences of the hero paragraph, and "What to wear." / "Pets." in the verdict details (everywhere, every state)'
wr_cond='Based on the coldest and warmest temperature, strongest wind and any rain or snow from now through the next 6 hours, so it covers weather on its way.'
for ph,wh in [
 ('It’s bitter out, so wear a heavy coat, [a warm hat / a toque], insulated [gloves / mitts], a scarf and warm waterproof boots.','Coldest hour under 15°F (−9°C).'),
 ('Bundle up with a warm coat, [a warm hat / a toque], [gloves / mitts] and a scarf, and wear warm boots.','Coldest hour 15–31°F.'),
 ('Wear a warm coat with [a warm hat / a toque] and [gloves / mitts], and layer up underneath.','Coldest hour 32–44°F.'),
 ('Dress in layers: a jacket or sweater now, and it warms up later.','Coldest hour 45–57°F and it reaches 68°F or more.'),
 ('Bring a jacket or a warm sweater.','Coldest hour 45–57°F.'),
 ('Dress light in breathable clothes, wear sunscreen and a hat, and bring water.','Warmest hour 85°F or more (and not cold).'),
 ('Light, breathable clothes will feel best, and sunscreen is a good idea.','Warmest hour 72–84°F.'),
 ('Light layers will do.','Otherwise (58–71°F).'),
 ('Wear waterproof boots with good grip for the snow.','Snow in the forecast right now.'),
 ('Snow is on the way, so wear waterproof boots with good grip.','Snow arrives later in the next 6 hours.'),
 ('Watch for ice: wear boots with good grip and take small steps.','Icy conditions and it is 34°F or colder (no snow).'),
 ('Bring an umbrella or a rain jacket.','Rain or showers right now.'),
 ('Rain is on the way, so keep an umbrella or a rain jacket handy.','Rain or showers arrive later in the next 6 hours.'),
 ('A windproof layer will help with the wind.','Wind of 16 mph (26 km/h) or more, unless it is below freezing.'),
 ('Comfortable shoes are a must for all that walking.','Big city, calm conditions (replaces the subway line).'),
 ('[Transit] or a cab beats a long walk.  ([Transit] is the city’s own: the subway, the Metro, the L, the light rail, a bus… see the Big city transit rows)','Big city with rain, snow, a coldest hour under 25°F, or wind of 25 mph (40 km/h) or more.')]:
    a(WR,wrw,ph,wh + ' ' + wr_cond,'At most two extra sentences are added after the main clothing sentence')
for ph,wh in [
 ('It’s dangerously cold for pets: keep them indoors except for quick potty breaks, and bring in any animals that live outside.','Coldest hour under 20°F (−7°C).'),
 ('Keep pets inside when you can, keep walks short, and wipe their paws afterward to clear ice, salt and snow.','Coldest hour 20–31°F.'),
 ('It’s chilly for pets, especially small or short-haired ones: keep walks short and consider a coat.','Coldest hour 32–39°F.')]:
    a(WR,wrw,ph,wh,'Pet safety')

a('Alert priority','Alert banner order, the Use caution tag and the verdict text','Tornado Warning, then Hurricane Warning, then Tornado Watch, then Hurricane Watch, then every other alert (warnings before watches before advisories, most severe first).','Several alerts are active at once (e.g. Pensacola with a hurricane warning plus flood and wind alerts).','The first one in this order is the alert named in the verdict text (e.g. "there is an active hurricane warning"). A tornado or hurricane warning always counts as the severe alert.')
a('Alert priority','Hero paragraph','No clothing or pet tips are shown while a severe alert is active.','Any Severe/Extreme alert.','The text stays about safety only')
a('Hurricane icon','Current Conditions weather icon, hourly strip, 7-day outlook and favorites card','One solid red spinning hurricane (six curved blades around a solid red center, turning counter-clockwise; still for reduced motion). Screen-reader label: Hurricane.','The forecast text mentions a hurricane, tropical storm, tropical cyclone or typhoon; the Current Conditions icon also switches to it while a Hurricane Warning or Tropical Storm Warning alert is active.','')
CA='Canada alerts'
a(CA,'Alert banner (Canada)','[Topic] [Warning / Watch / Advisory], e.g. "Frost Advisory"','An Environment Canada warning, watch or advisory is active for the nearest forecast location.','Yellow alerts count as Moderate, orange as Severe (so the verdict shows Use caution), red as Extreme. Special weather statements are not shown.')
a(CA,'Alert banner details','Issued by Environment and Climate Change Canada. Read the full alert, with details and what to do, at [link].','Every Canadian alert.','Canadian alerts link to the full text at weather.gc.ca')
a(CA,'Radar (Canada)','Looping last hour of national radar (6-minute frames); no expanded or forecast radar','Any Canadian location.','')

CV='Canadian voice'
cw='Hero paragraph (visitors in Canada only)'
cond_ca='Visitor has a Canadian time zone or language, or is viewing a Canadian place; never used under a Severe/Extreme alert.'
for ph,wh,n in [
 ('Beauty day, eh? [Day] [time] is a great time to get outside. / Give’r! [Day] [time] looks like a beauty. / [Day] [time] is a beauty of a time to get outside, don’t you know.','Verdict is Yes and comfortable.','Replaces the three standard Yes openers'),
 ('[Day] [time] works for getting outside, eh? / Not bad at all: [day] [time] is a good time to get outside, eh?','Verdict is Yes but not especially comfortable.','Replaces the two standard openers'),
 ('You can head out right now, though conditions aren’t the dreamiest, eh.','Verdict is Maybe and the window starts now.',''),
 ('[Why it is not good right now], so hang tight, eh: [day] [time] looks like a lovely time to get outside.','Verdict is Maybe with a window later today.',''),
 ('It’s a beauty of a day to [activities] / Time to [activities]','Yes/Maybe with a fitting activity.','Two of the four activity lead-ins'),
 ('Keep your toque handy.','Average temp under 7°C (45°F) in a Yes or Maybe window.','One extra sentence, chosen by the date'),
 ('The maple leaves should be putting on a show, too.','September to November, little chance of rain.','One extra sentence, chosen by the date'),
 ('Might be worth a loonie or two for an ice cream.','Average temp 27°C (80°F) or higher.','One extra sentence, chosen by the date'),
 ('Give’r!','Dry ground and almost no chance of rain.','One extra sentence, chosen by the date'),
 ('[Today / This morning / This afternoon / This evening / Tonight] is a bit of a gong show out there: [reasons] / Bit of a gong show outside right now: [reasons]','Verdict is No with two or more reasons, or wind of 25 mph (40 km/h) or more.',''),
 ('There’s a bit of a weather kerfuffle going on right now: [reasons] / Even the Mounties would sit this one out: [reasons] / [Today / This morning / This afternoon / This evening / Tonight] is a cozy-inside kind of moment: [reasons]','Verdict is No (milder reasons).',''),
 ('There’s no good outdoor activity window in the next [3 / 5 / 7] days, so it’s a fine time for a movie and a double-double from Tim Hortons. / ... and pancakes with real maple syrup.','Verdict is No with no window in [3 / 5 / 7] days.',''),
 ('[Today / This morning / This afternoon / This evening / Tonight] is dark, eh, so most outdoor activities will be a challenge unless you’ve got a good headlamp.','Night time tag, small town.','Replaces one of the six standard openers'),
 ('Stargazing is free, so save your loonies and toonies for tomorrow’s coffee. It’s [calm/breezy] and [clear/partly cloudy] out there.','Night time, small town, clear or partly cloudy sky.','Replaces one of the three standard star lines'),
 ('Bring your toque if you do step out.','Night time and under 10°C (50°F).','Extra sentence')]:
    a(CV,cw,ph,wh + ' ' + cond_ca,n)
for v,c2 in [('walk → stretch your legs for a few clicks','Walking'),('run → run a few clicks','Running'),('bike ride → go out for a rip on your bike','Cycling'),('picnic → have a picnic with something drizzled in maple syrup','Picnics'),('al fresco → enjoy a Tim Hortons coffee on a patio','Dining al fresco')]:
    a(CV,'Activity verb (visitors in Canada)',v,'Half of the time, for visitors in Canada.',c2)

a('Footer','Bottom of the page, under “Data as of”','Copyright © 2027 Check The Wind','Always shown.','Standard copyright notice; the year is written into the page')

C='Consent banner'
a(C,'Bottom bar, first visit','Help us count visits? We use Google Analytics to see how many people use Check the Wind and which features they use. It’s for analytics only, with no ads. [What we track]','Shown until the visitor chooses; hides after Accept or Opt Out and is remembered.','Buttons: Opt Out / Accept')

import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','phrasing.csv')
with open(OUT,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Area','Where it appears','Phrase (brackets are filled in)','When it appears','Notes']); w.writerows(R)
print(len(R))
