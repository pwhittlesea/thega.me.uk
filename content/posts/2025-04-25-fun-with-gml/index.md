---
title: "Fun with GML"
date: 2025-04-25 14:07:00 +0100
last_modified_at: 2025-04-25 13:59:35 +0000
category: [code]
tags: [engineering, maps]

summary: "Four 'fun' GML problems that pop-up when working with GML in the wild."
---

After the best part of a decade working with data in the geospatial and aviation domains, I thought I would write about some fun data problems I encountered.

## Introduction

When I started my career &mdash; in 2012 &mdash; I began by working on an {{< term "XML" >}}-to-database conversion tool.
This tool existed primarily to assist those looking to consume the large volumes of OS MasterMap ({{< term "OSMM" >}}) data produced by [Ordnance Survey](https://en.wikipedia.org/wiki/Ordnance_Survey), by loading said data into a spatial [Oracle](https://en.wikipedia.org/wiki/Oracle_Database) database.

OSMM was distributed as highly detailed {{< term "GML" >}} (Geography Markup Language) &mdash; a standard XML-based format for encoding geographic information &mdash; files, allowing for a standardised exchange of the information within them.

OSMM contains features which record information on real-world objects;
everything from phone boxes to rivers.
Each feature contains lots of properties (like a name), but the most valuable thing was that it stored was the location and dimensions of each object.

In the United Kingdom (UK), councils would use this data to check what would be affected by planned building works.
If you were a building company, which needed to ensure you were aware of any obstructions, you would buy this data _before_ you started building[^1].

[^1]: I could probably write a whole blog on designing datasets that can return you the answer to the question "What data would we have given someone if they asked for it 4 weeks ago".
      Councils in the UK frequently have to deal with retrospective planning permission requests.

As I joined, the customer base broadened to companies outside the OSMM ecosystem.
GML (or ISO 19136) is a standard and the tool allowed for generic XML mapping, so it was useful for more than just OSMM.

Most of my time was spent on the 'geographic' part of this problem, as there are lots of weird and wonderful ways that the human-entered geometries used day-to-day, are not tolerated by spatial databases.

Here are my top four fun things which I encountered.
My favourite will always be 'putting the wrong unit of measure in', but here are some of the more interesting ones.

## Lat/Lon or Lon/Lat

I think the biggest way in which GML is 'wrong' is the latitude and longitude being the wrong way around (or being read the wrong way around).

Within GML, you have to define a 'Spatial Reference System' ({{< term "SRS" >}}) which defines how the points you encode are interpreted and mapped to the Earth's surface.

Every SRS has bounds and a center point; from where 0 is measured.
The SRS I have seen used most frequently is WGS 84 &mdash; the global standard for GPS coordinates &mdash; which defines the world from `-180, -90` to `180, 90`.

![Image showing a map of the world and a blue box showing the bounds of the EPSG:4326 reference system](bounds_epsg_4326.png "Source: https://spatialreference.org/ref/epsg/4326/")

You also have OSGB36 (or [`{{< term "EPSG" >}}:27700`](https://spatialreference.org/ref/epsg/27700/)) which is specifically used in the UK by our national mapping agency, which defines the bounds from `0, 0` to `700000, 1300000`.

![Image showing a map of the United Kingdom and a blue box showing the bounds of the EPSG:27700 reference system](bounds_epsg_27700.png "Source: https://spatialreference.org/ref/epsg/27700/")

Many countries have their own SRSs to ensure local features are mapped accurately.

Ordnance Survey have some wonderful pages that dive deeper into this better than I can (with some really helpful pictures).
Their [page on myths](https://docs.os.uk/more-than-maps/deep-dive/a-guide-to-coordinate-systems-in-great-britain/myths-about-coordinate-systems) and their page on [the shape of the earth](https://docs.os.uk/more-than-maps/deep-dive/a-guide-to-coordinate-systems-in-great-britain/the-shape-of-the-earth#ref505694403) are great if you want to know more!

A coordinate like `50.909662, -1.405141` means nothing by itself.
You could _assume_ that it is a lat/lon in WGS 84, and in this case you would be presented with the Cenotaph, in my hometown.
However, the numbers could also represent a lon/lat, and the location would be off the coast of Somalia.

The SRS encodes if longitude or latitude should be first, but that doesn't stop humans from getting it wrong (or software for that matter).

It would have probably been simpler to introduce a specification which didn't make this mistake possible.
Well the story I was told &mdash; which I cannot find independent verification for online, so it might be folklore &mdash; is that the original GML spec did define only one way to order latitude and longitude, but the examples in the document were the wrong way around.
By the time anyone had figured it out, it was too late.
Some followed the specification, others copied the examples;
everyone had picked a way and started working with it.

## Reference Geometries

One of the more complex cases when loading GML comes when you have 'referenced' geometries.
When defining the geometry representing a feature, humans tend to take shortcuts.

For example, if a cartographer was defining a field that runs up to a river, they might define the following:

> From the gate the field runs 200 meters north, then west to the river, then it follows the bank of the river south for 200 meters, before coming back to the gate.

This is normally how the world works.
If the bank of the river moves, the field doesn't extend into the middle of the river;
the field contracts to the new bank of the river.

This makes using the data much harder in systems that don't handle references (like databases).
Datasets frequently won't tell you the section of the river that applies, you have to look it up in another part of the data, and extract the relevant part.

Programmatically this is a trivial intersection of two geometries, but becomes much harder when the geometry that is referenced might not be in the same file you are loading.
The reference might be hosted online, in a later file on the same {{< term "CD" >}}, or might not even have been digitised yet.

```xml
<gml:FeatureCollection
      xmlns:gml="http://www.opengis.net/gml/3.2"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <gml:Point gml:id="end" srsName="urn:ogc:def:crs:EPSG::4326">
        <gml:pos>2.0 2.0</gml:pos>
    </gml:Point>
    <gml:Geodesic>
        <gml:pointProperty>
            <gml:Point gml:id="start" srsName="urn:ogc:def:crs:EPSG::4326">
                <gml:pos>1.0 1.0</gml:pos>
            </gml:Point>
        </gml:pointProperty>
        <!-- This is where the pain begins -->
        <gml:pointProperty xlink:href="#end" />
    </gml:Geodesic>
</gml:FeatureCollection>
```

Then the geometry might be in a different SRS, which then necessitates conversion.

For my work, this became an expectation management task with our customers.
You have to draw a line somewhere (pun intended).
We allowed references to features on the same CD but nothing else.

This becomes even harder when you encounter geometries which don't align perfectly.

## The Puzzle Pieces Don't Fit Together

One that would happen all the time, would be that the parts of a geometry wouldn't form a complete _closed_ polygon.

This is an issue because databases such as Oracle/PostgreSQL, don't support them, and this is where our mapping tool was supposed to write them.
Databases are intentionally not fault-tolerant because when you assume how a polygon should close, you might introduce errors which may lead to catastrophic problems[^2].

[^2]: Of course you can fly over that military airspace, the polygon wasn't closed!

A non-closed geometry can happen for many reasons, to name a few:

1. The {{< term "UoM" >}} might be wrong, maybe through the use of non-{{< term "SI" >}} units (like `m` for mile when it should be `mi`).
2. The referenced geometry (like a river) didn't have a point precisely where another line met it.
   When you take the line(s) that are needed, they still don't meet.
   ![Image showing a polygon and a line where the line does not intersect at a known point](river.png)
3. Referenced geometries that don't intersect at all.
4. Just plain old bad input data that specified non-closed points.

The solution was to implement auto geometry closure.
Customers could set a distance where they deemed geometries safe to close.

Two points that are 3 cm away from one another on a polygon 30 kilometres wide?
Probably fine.
Two that are 30 kilometres apart?
Let's take a closer look.
A non-closed military operation area?
Well...

This was one of those problems that's easy for humans to look at visually, but hard to get a machine to solve autonomously.
Do you put a new line in the gap?
Do you cut one line down if it's too long, or extend one out if it's too short?

![Image showing a good and bad closure of a triangle](closure.png)

## Interpolated Geometries

These were always the most fun!

When defining a geometry in real life, humans often don't want to define a line with lots of points.
Often we want to say 'a circle around X', or 'and arc from A to B to C'.
This happens a lot in Aviation.

If we take the example below of Gatwick Airport, we have one circle for the inner airspace, and two arcs at either end of the outer airspace:

![gallery-1](london_gatwick.png "The Airspace around London Gatwick &mdash; Source: [https://skyvector.com/](https://skyvector.com/)")

The west arc is 17 kilometres wide;
it's much better to define it as an arc than to digitise it with thousands of points.

GML (defined [here](https://schemas.opengis.net/gml/3.2.1/geometryPrimitives.xsd) if you read XML schemas) contains lots of complex geometry types which do not themselves have points, but instead convey an [interpolation](https://en.wikipedia.org/wiki/Interpolation).
I have seen a `Arc`, `Circle`, `ArcByCenterPoint`, `CircleByCenterPoint`, `Geodesic`, and `OffsetCurve`[^3] used in aviation.

[^3]: A line that is 'offset' from another by a given amount.
      Very useful for defining flight corridors.

There are other types (like a [`Clothoid`](https://en.wikipedia.org/wiki/Euler_spiral)), but I have never seen one in the wild.

You probably guessed it, but a spatial database wants none of these complex types.
Before loading one of these types they need to undergo a process called 'densification' &mdash; converting interpolated geometries into a collection of points connected by lines.

![Image showing a curve with different densification granularity](densification.png)

This process takes quite a bit of customisation depending on your use case and the size of the geometry in question.
You want to balance the amount of detail you keep (a circle has infinite detail), and the volume of the data you generate.
More points might mean terabytes of data, but fewer points might mean that the geometry doesn't cover the area you want any more, and you don't flag up a flight that is 100% coming into your airspace.

## Fin

Thanks for reading!

If you know more about this domain than I do, and you notice something wrong;
reach out, and I will fix any inaccuracies.
