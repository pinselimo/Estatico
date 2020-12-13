# On narrow roads through Sars-CoV-19

## Creating space amongst people whilst obeying conservation laws of physics

Say goodbye to life as we know it.[\[1\]](https://www.youtube.com/watch?v=uz8kH24iwa4) For a while. I've gone into this quarantine on my first day after sick leave. Consequently, after one week of Q I hadn't left my flat for two weeks straight. With time the feeling of being locked into this place grew. So eventually I went for a run; With many more to come in the past weeks.

I try to start my runs at around 7:20 AM. Early enough to avoid the shopping window for the elderly and people in general. Yet I somehow end up running a weird mix of slalom and hurdles as I swerve around the pedestrians. Most sidewalks in Graz are, if existent, too narrow to keep enough distance. So one ends up jumping from sidewalk to street and back, exchanging one risk for the other.

### Swerving

So who can show us a way around this problem? [Vienna](https://coronavirus.wien.gv.at/site/mehr-raum-zum-rausgehen/) has turned some roads into pedestrian zones (temporarily). [In Berlin](https://www.spiegel.de/auto/der-autoverkehr-ruht-kreuzberg-schafft-fakten-a-4b8a8e18-0ad4-409c-88fe-23a5b16e2e9b) some roads were partially devoted to bike riders. [In Milano](https://www.theguardian.com/world/2020/apr/21/milan-seeks-to-prevent-post-crisis-return-of-traffic-pollution?fbclid=IwAR3xvcAa7hPWp2-Oq1_u4YFVO46YUH9klD2e8ervk6xZV8tliOITDdqb_R4), the epicentre of the European Corona crisis road space is allocated to pedestrians and cyclists. And in Graz... 

In Graz your parking spot might as well [extend over half of the sidewalk](https://www.meinbezirk.at/graz/c-lokales/kurzparkzone-statt-gehsteig_a4027800). No worries, parking has been made free for the first month of quarantine, so you can block the sidewalk all day long! Apparently, no intentions to change anything.

Fortunately, I have a traffic model at hand to show me a glance of realities I cannot get.

### Bird's eye view

First a brief introduction. Let's assume you have a map of your respective city. In our case that's Graz and for our map service we use [OpenStreetMaps](https://www.openstreetmap.org/search?query=Graz#map=13/47.0721/15.4375). Now you just blend everything out but the roads you could legally drive a car on. Consider all intersections and points of interenst vertices and the roads in between them as edges et voilá: You have a road network representation of the city. *(Shoutout to Goeff Boeing for providing the awesome [OSMnx](https://github.com/gboeing/osmnx) tool)*

![Fig.1: Congestion at 7 AM in the City of Graz in the before times, according to our model](images/corona_graz_before.png)

Now slap an agent per citizen onto the network, add some commuters for the right flavour of rush hour, run your simulation and you got yourself the congestion patterns arising according to the underlying model. (See Fig. 1) What you're looking at right there is what rush hour (7 AM, weekday) meant in the beforetimes. Grey depicts little traffic, green is traffic worth considering and the more the colours go towards a red, the heavier the congestion.

But with the nation wide lockdown, PMT traffic numbers dropped significantly. For Vienna the responsible agency reported a decrease of [52% in car traffic](https://kurier.at/chronik/wien/wegen-corona-massnahmen-verkehr-in-wien-ging-stark-zurueck/400806389). Google provides weekly updates on the mobility change due to the novel corona virus. [Initially](https://www.gstatic.com/covid19/mobility/2020-04-11_AT_Mobility_Report_en.pdf) mobility for recreational purposes decreased by over 80% in Austria. [By now](https://www.gstatic.com/covid19/mobility/2020-04-17_AT_Mobility_Report_en.pdf) more shops have opened and the reductions has recovered to some 60%. However, still a drastic reduction.
Finally, a study of the ETH Zürich shows that people somewhat shifted their mode choice [from car to bike rides](https://ivtmobis.ethz.ch/mobis/covid19/reports/latest_de). While it's not clear whether these rides fulfill the same objective, it is obvious that the space allocated for the means of transport is more misdivided than ever before.

How do we get these insights into the model? Since the only mode of transport we are interested in for urban congestion is personal motorised transport, we'll focus on cars. The data for our model is drawn from the survey ["Österreich Unterwegs 2013/14"](https://www.bmk.gv.at/themen/verkehrsplanung/statistik/oesterreich_unterwegs/ziel.html). Fortunately, in this survey all journeys are also categorised by their purpose. Thus, I will use the ratios from Google to adjust for our new demand model. For some categories which do not align with those of Google I have to take educated guesses. Glad this isn't a scientific paper. Here is a table with the travel purposes and their respective adjustment:

<table>
  <thead>
    <tr>
      <th>Purpose</th>
      <th>Ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Recreation</td>
      <td>0.37</td>
    </tr>
    <tr>
      <td>To work</td>
      <td>0.5</td>
    </tr>
      <td>Going home</td>
      <td>0.5</td>
    </tr>
    <tr>
      <td>Business trip</td>
      <td>0.5</td>
    </tr>
    <tr>
      <td>Shopping</td>
      <td>0.4</td>
    </tr>
    <tr>
      <td>Private visit</td>
      <td>0.01</td>
    </tr>
  </tbody>
</table>

If we consider this change in travel demand, we can plot the arising congestion according to the same traffic model we used for figure 1. Commuters are considered travelling to work places, thus according to Google's data reduced by 50%. The result of such a simulation can be observed in Figure 2.

![Fig.2: Simulated congestion in Graz after the effects of the corona lockdown](images/corona_graz.png)

As expected, congestion decreases when we reduce the travel demand of the inhabitants. Let's inspect what we can do with this information. But first:

### Disclaimers

+ What's the best thing about a model? 
    We can try whatever scenario we can think of. Consider it the escapism of modern times.
+ What's the caveat?
    A model is not reality! It's most often a vast simplification. It gives us a *direction* not a definite answer. Consider it sort of the oracle of modern times.
    
(The model put to use here is an unpublished new version of our [previous model](https://www.researchgate.net/publication/333438552_Mesoscopic_Urban-Traffic_Simulation_Based_on_Mobility_Behavior_to_Calculate_NOx_Emissions_Caused_by_Private_Motorized_Transport)

### Going with the flow - a vision

Now we can go on in constructing our new urban road policy. Obviously, we cannot just close all of the roads below tertiary level completely. Yet we can make them safer for pedestrian and cyclist's use. My proposal is quite simple: Reduce the speed limit on minor roads to 20 km/h. Furthermore, for every minor road with two or more lanes one lane will be devoted to pedestrians and cyclists.

![Fig.3: Highway tags of roads in Graz, red is the highlighting colour](images/hwtags_graz.png)

One way to categorise roads is by their respective "highway" tag (given by OpenStreetMaps contributors). In figure 3 you can see the most important roads for our analysis. Red is the highlighting colour, if you're wondering. For now, just keep in mind that most of the roads below tertiary level are categorised as "residential". With some being left for the tags "living-street" and "unclassified". We'll just throw those into a single bin together for now. These are the minor roads I am speaking of. For roads of secondary level I propose to introduce a speed limit of 30 km/h. 

Such advances are not there to annoy car drivers. While at first they might, subsequently they change our perception of the road network. The fastest route to some place might no longer be the one we chose before. Thus, a new equilibrium state of congestion arises, which is what our model tries to simulate. So if we put these policies into action and let things settle down, we could end up with something close to what is shown in figure 4.

![Fig.4: Congestion once we devote more space to pedestrians](images/corona_scen1.png)

What if the demand switches back to one similar as observed in the before times? Well as for what our model has to say to this, take a look at figure 5. Congestion is show to be drastically increased. Also on the highway circumventing the City of Graz. 

![Fig.5: Congestion once we devote more space to pedestrians and traffic demand falls back to how it was before](images/corona_scen1_olddata.png)

### Con-close-io

Soon the lockdown will be over, but the required distance among people will be kept in place. Consequently, we can expect even more people on the sidewalks. Probably we will also see more cars on the roads again. We might have just missed the perfect time to shift peoples mobility behaviour towards more sustainable modes of transport. It is times like these, where people can open there minds towards change. They have to. Many people are forced to reduce their time spent outside their homes to bike rides and walks. Now more than ever we can see the value of space in our cities. 

So what's the take-away from my blog post? What's the story of these simulation runs? 

My aim was not to show what the world would look like if we closed roads and reduced speed limits. I cannot stress enough how limited such a model is in telling us things about the world around us. I just wanted to seed an idea, to show that the world would not collapse if we tried something new. Something radical in a time of forced radical change.
