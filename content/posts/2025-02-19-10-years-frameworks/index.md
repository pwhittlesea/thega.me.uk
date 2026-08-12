---
title: "Looking back - 10 years writing application framework code"
date: 2025-02-19 15:00:00 +0000
last_modified_at: 2025-04-27 11:49:52 +0000
categories: [code]
tags: [architecture, engineering, "code quality"]

summary: "What have I learned after 10 years of writing application framework code?"
---

After a decade of designing, building, and maintaining an application framework for real-time data processing applications, what have I learned? What assumptions did I make ten years ago that were vindicated, and which did not stand the test of time?

## Background

> [!INFO]
> If you aren't interested in the back-story, and want to jump to what I have leaned, you can skip [here](#what-have-i-learned).

Inspired by [this post by Chris Kiehl](https://chriskiehl.com/article/thoughts-after-10-years) &mdash; which you should go read &mdash; I began thinking about what lessons I had learned over the last ten years of my career.

A decade ago I was a Software Engineer, three years out of the University of Southampton.
I had a passion for the craft of software engineering; how could we build pipelines and use the tools available to ensure that when we shipped software, we knew it worked.

Now, I'm Lead Architect for [Cirium](https://www.cirium.com/), and I spend my days designing enterprise solutions which span the whole business.
I'm not supposed to write software anymore, but sometimes I need a break from Excel spreadsheets and Teams calls; so I crack out my {{< term "IDE" >}} and pick up my passion project - A real-time Kafka-based application framework.

## What do I mean by 'Application Framework'?

To first explain what I mean by 'Application Framework', I first have to explain 'why an Application Framework'.
What is its reason for existing that something off the shelf could not provide?

Back in 2016, Snowflake Software (now Cirium), processed data from many sources.
This data came in disparate formats, which all needed homogenising and fusing into a single domain object.
We might get data about the location of a flight from one source, and the planned route of the flight, from another.
We then produced a multitude of datasets that combined all these sources together to provide insight to customers.

This is of course _massively_ over simplifying what we did, but the important point is we were doing a **lot** of real-time {{< term "ETL" >}} operations.

To make our product easier to work on (and debug), we opted for building single-purpose [Microservices](https://en.wikipedia.org/wiki/Microservices), with a [Kafka](https://kafka.apache.org/) message-bus glueing it all together; allowing us to see the data at each stage of processing.

As an example:

1. A 'connector' pulls data from a source and places it on Kafka unchanged.
2. A 'normaliser' would take XML data from a data provider and convert it into an internal JSON interchange format.
3. An 'enricher' would add additional contextual information (e.g. the phase of the flight, based on speed and altitude).
4. And so on...

Now, it's no secret that microservice architectures transfer the complexity from the code into the operation and deployment of the system, but the downside we noticed first is that when you write lots of microservices, you end up with a lot of code that looks the same.

There are whole 'rule books' on what behaviour each microservice should exhibit.
[The Twelve-Factor App](https://12factor.net) probably being the one I reference the most.

> A twelve-factor app never concerns itself with routing or storage of its output stream. It should not attempt to write to or manage logfiles. Instead, each running process writes its event stream, unbuffered, to `stdout`.
>
> &mdash; [The Twelve-Factor App](https://12factor.net/logs)

Once one, twenty, or fifty of your microservices want to log to `stdout`, want to read and write from Kafka, and want to publish metrics, you end up with a lot of configuration that looks the same.

Off-the-shelf frameworks like [Spring Boot](https://spring.io/projects/spring-boot/) solve the 'how' of these functions &mdash; giving you a `KafkaTemplate` to write to Kafka, for example &mdash; but as off-the-shelf tools they don't prescribe your businesses desired configuration of those functions.

Questions like 'how do we name consumer groups', and 'what message payload do we send', and 'what prefix do I use for metrics', pop up every time you write a new microservice.

You could, for example, configure a different prefix for metrics in every single microservice (which we did) to ensure you can differentiate them.
This seems sensible to start with, until you realise you can't graph all the metrics together easily, and you should have used a tag instead.
Without some central management of config, you have to update each of the apps to the new behaviour.

Spring Boot and other frameworks don't have an opinion of how your business wants to run their applications, allowing an unbounded combination of configurations.

An '_Application Framework_' in my context, is the codification of those business opinions.
It limits the choices developers can make about what they build, constraining them to achieve a homogenous ecosystem across all your applications.

![application-framework](application_framework.png)

An application framework adds a layer on top of off-the-shelf frameworks that is concerned with how your businesses applications should run.

Importantly, it should make it easy to build the right thing.
That is, developers should _want_ to use it, because it makes their lives easier.
No one actually wants to make sure that the upstream latency metric is working on each component, or that every log line is JSON; they just want to write the cool business logic that analyses airspaces.

That business logic is actually where the **value** of your business is located.
Customers are not paying you to have the best Kafka serialisation code, or a metrics library that adds the correct tags.
The less time you spend duplicating Kafka test harnesses, the more time you can dedicate to making sure the business logic passes its behaviour tests.

## What did I build?

> [!NOTE]
> Although this section is called 'What did I build?', I cannot claim that I did build it all myself.
> I have worked with some very talented engineers over the years who all helped add and improve this framework.
> As always, it's a team effort.

Back in 2016 we were building lots of microservices, creating libraries to handle some common functions like metrics.
We had somewhere in the region of thirty at the time, but I was predicting that we would hit one hundred within a couple of years.

From a maintenance perspective, this was concerning.
We would have over a hundred applications which were configuring Spring Boot, [Spring Kafka](https://spring.io/projects/spring-kafka), and [StatsD](https://github.com/DataDog/java-dogstatsd-client); all of which would require updates as breaking changes arose or behaviour changed.

At the time I watched a talk &mdash; one which I cannot find since, so I might have hallucinated it &mdash; after I attended [Microservices Manchester](https://www.opencredo.com/blogs/microservices-manchester-conference-recap), where the presenter said something akin to:

> As an application developer, just put me in a box.
> I don't care about where configuration comes from, where logging or metrics end up, or how events are routed.
> I just want APIs which abstract away the complexity of how these services are provided.
>
> &mdash; Someone

Something in this statement called to me.

I went home and begun working on a prototype of the application framework which would become the core of every application that was built within the business.

The premise was simple.
An engineer would create a Maven project and add a dependency on the framework.
They would then write a 'consumer' class, annotate it with a [Spring annotation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Component.html) for autowiring, and voilà!

```java
/** Simple transformer example. */
@Component
@Slf4j
public MyConsumer implements InboundProcessor<MyPayload> {

    @Autowired
    private OutboundDispatcher outboundDispatcher;

    @Override
    public void process(final InboundEvent<MyPayload> event) throws InboundProcessorException {
        // business logic goes here
        if (event.isCool()) {
            log.info("Doing some important work");
            event.incrementCoolness();
            outboundDispatcher.dispatch(event)
        } else {
            throw new InboundProcessorException("Something has gone wrong");
        }
    }
}
```

You would need to bring-your-own domain object (`MyPayload` in this example) and configure some properties (like which Kafka topic to read from), but that was about it.
The application would start up and your business logic class (`MyConsumer`) would start receiving messages.

Sure, it's a very thin layer on top of Spring Kafka, but the engineer didn't need to worry about `KafkaConsumer` or `KafkaProducer` setup, how acknowledgements work, or how messages are serialised and deserialized from the on-the-wire format.

They concentrate on building, and testing, only the logic needed to give the microservice its behaviour.

The framework could handle retries, batching, latency metrics, health checks, etc.

The 'pièce de résistance' however, was the simple test framework that accompanied it:

```java
@EventFrameworkTest
void MyConsumerIT {

    @Test
    void testMessage(FrameworkEnv env) {
        // GIVEN an inbound message
        final MyPayload in = new MyPayload();
        in.setCoolness(59);
        env.sendToTopic("inbound", in);

        // THEN an outbound message is received
        final MyPayload out = env.getFromTopic("outbound");
        assertThat(out.getCoolness()).isEqualTo(60);
    }
}
```

The sheer volume of lines `sendToTopic` and `getFromTopic` replaced was unbelievable.

I put a very quick example together of an application using this, and one not using this.
Being able to strip 90% of the tests and production code out into a well tested library is very compelling.

## What have I learned?

So with all of that, back to the point of this blog.

After ten years of maintaining this framework, what have I learned?

(In no particular order of priority)

### Seek a common vernacular

You will have noticed I've used some words above like 'connector', 'normaliser', and 'fuse'.

To have highly technical conversations, you need simple ways of communicating common concepts:

Connector
: A microservice which pulls data from an external source and places the response on Kafka unaltered.

Normaliser
: A microservice which reads raw data and converts it into the internal interchange model (normally JSON).

Fuser
: A microservice which aggregates data together to create a single view.

These names may seem logically intuitive, but it actually requires a concerted effort to nudge people to using these terms.
Once you get there however, you are able to side step a lot of the description and jump straight to an understanding.

The framework I described above is known internally by a name I coined after using a random name generator.
It may seem silly &mdash; it _is_ intentionally so &mdash; but having a recognisable name that has zero overlap with existing solutions, gives you a 'brand' that engineers can easily recognise.

The framework itself supports four different types of application, which we also picked clear, unambiguous names for:

Sink
: A microservice that only receives Kafka events.

Source
: A microservice that only generates Kafka events.

Transformer
: A microservice which receives and then generates events.

Blank
: A microservice which has all the common functionality but does not handle events.

Having these common descriptions of functionality allows you to say 'oh, we need a new transformer, a connector for the raw data'.

This worked _extremely_ well to not only simplify discussions, but its usefulness stretched to finding code in GitHub.
For example, searching for 'connector FAA' would allow you to find all the applications that connect to the FAA and consume data.

This can also be beneficial outside the engineering team.
Finding common language for software quality, like what 'alpha' means for your customers experience, allows you to work with sales and product departments to manage customer expectations.

### Make the right thing easy

As I said above, a good framework should make building whatever an engineer sets out to build, easy.

When someone sets out to build a new application, there should be no question about using the framework; the benefits it gives far outweigh any loss of autonomy.

### There is value in limiting choice

Engineers can do anything.
There are many ways to write the same piece of code.

Just look to the [configurability of common code formatters](https://checkstyle.org/property_types.html#LeftCurlyOption).

Brackets on the same line, or a new one?
Maybe even no brackets at all?

The normal advice I see is to 'keep style consistent', but after watching engineers work on applications for over a decade, this does not come naturally.

My [#1 rule]({{< ref "2024-05-25-rule-one" >}}) is to programmatically enforce things that you care about, and style is one of those things.

For the best part of the last decade I used [CheckStyle](https://checkstyle.org) which only complains if the engineer gets the style wrong; however this leads to resentment when CheckStyle is whining at you.
So more recently I switched to [Spotless](https://github.com/diffplug/spotless), which can re-format the code as well; making 'compliance' as simple as `mvn spotless:apply`.

Beyond code style, there are also many ways you can write code to connect to Kafka, output logs, and generate metrics.

Providing a library to handle these things is a common way to keep your code base [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself) &mdash; a principle I have [issues with](#its-ok-to-repeat-yourself) &mdash; but most engineers will seek to add lots of options 'just in case'.
I however find value in maximising work not done, and leaving configurability until someone can give me a good reason to stray from the path given.

### Your framework needs a gatekeeper

The framework described above, has a very specific remit: handling the most common set up for our microservices, so engineers don't have to.
This includes (but is not limited to) very basic things, like logs, metrics, handling Kafka messages, and JSON serialisation/deserialisation.

There have been times in the past where an engineer has been handling a very complex use case, like deserialisation of geometries, and has asked for the framework to include geometry handling code.

As a business, Snowflake Software did build a lot of geometry focused code, but it was mostly contained within a couple of microservices.

Do you extend the framework to include geometry parsing, as a result making it more complex?
Or do you push back, and tell them to write a library if they want it in more than one place?

The key question for me has always been, does this feature need to be done to achieve the 'very specific remit'.
If not, then you can do it in user-space.
Will every application be doing this activity, or is it less than 10% of the problem space?

The reason to push back is maintainability and rate of change.

For every feature (read behaviour) you add, you then have to test and maintain it.
It's one more thing that you have to provide backward compatible changes for, one more thing to patch.
It broadens your likelihood of getting a {{< term "CVE" >}} if it includes new libraries, and increases churn if it's a new feature which is still having its behaviour ironed out.

An application framework needs to be clear about what it does, but clearer about what it is not supposed to do; otherwise you end up with a swiss-army knife of chaos[^1].

[^1]:
    One way you can bat away demands is to build in extension APIs to the core parts of your framework.
    For example, we added a `SerialiserConfigurer` which would be called at start up to register additional serialisation code, if required.

    If someone wanted to add additional geometry serialisation code, they could use this extension and have the code loaded at start up by leveraging a Java `ServiceLoader`.

### Maintainability beats cleverness

I have written some very clever code in the past.

I have seen some astonishingly clever code written by others.

But being clever is one way to write some code, and in my experience, there is normally another way to write it that is more readable.
Take the following trivial example:

```java
String status(boolean failed, Exception e) {
    return failed ? e instanceof RecoverableException ? "Recoverable Failure" : "Unrecoverable Failure" : "Success";
}
```

A one line method, nice.
Some engineers value fewer lines of code because of the &mdash; frankly perplexing &mdash; idea that it results in less bugs.

You may be a 9^th^ level ternary mage, but most people find `if` statements easier to read.
`if` statements also give more space for comments, to help with understanding[^2].

[^2]:
    If I were to write a 'Rule #2' it would be that self-documenting code is a lie which lazy programmers like to roll out whenever you ask them to explain what their code does.

    If you cant write a comment explaining briefly what the code is supposed to do, then when someone comes back in a year, or ten, what hope do they have of understanding it?

Consider the alternative:

```java
String status(boolean failed, Exception e) {
    if (failed) {
        // Is the exception recoverable?
        if (e instanceof RecoverableException) {
            return "Recoverable Failure";
        } else {
            return "Unrecoverable Failure";
        }
    }
    // There is no failure
    return "Success";
}
```

Yes, it is more verbose, but when this pops up in my IDE while debugging, I can almost instantly follow the process flow[^3].

[^3]:
    There is probably an exception for applications where every CPU cycle is precious, so you would want to write the most optimal code, but I will always request changes in PRs to make the code more readable.

I am aware this is a pretty convoluted example.
Most 'clever' code I see comes from an over-application of the design patterns book they make you read in university, but that would be difficult to fit on an example here.

In my experience, engineer skill sits on a [bell curve](https://en.wikipedia.org/wiki/The_Bell_Curve).
A given company may have some extremely capable engineers, but they will have a far greater number of 'just' good engineers.
The code you write should be maintainable by the average engineer to ensure that the code is approachable by most of your company.

'{{< term "KISS" >}}' has been around forever, so don't burden those following you with displays of your coding prowess.
No one likes a show-off; keep the code simple where possible.

### It's OK to repeat yourself

As we know, all 'rules', when overused, cease to become useful.
DRY is that rule for me.

DRY seems to be taken at face value by most engineers, inevitably causing them to take it too far, making code less readable in the process.
[AHA (avoid hasty abstractions)](https://en.wikipedia.org/wiki/Don't_repeat_yourself#AHA) and [WET (write everything twice)](https://en.wikipedia.org/wiki/Don't_repeat_yourself#WET) are better because they are not absolute.

Where DRY has no business being, is in test code.
Test code should be free of branching and conditional logic; otherwise you have to test your test code[^4].

[^4]: [Mutation testing](https://pitest.org/), anyone?

If you have twenty tests which all need an input object, it's tempting to create a function like `setUpTestObject()` to create one.
This works well, reducing the lines of repeated code.
However, the twenty-first test requires one of the properties be different.
What do you do?

Some engineers will add a parameter to the test function, maybe a `if` statement to create one property if `true`, and another if `false`:

```java
@Test
void testFlightWithoutPlan() {
    Flight flight = setUpTestObject(false);
    // the rest of the test
}

private Flight setUpTestObject(boolean planned) {
    Flight flight = new Flight();
    if (planned) {
        FlightPlan plan = new FlightPlan();
        // complex plan setup
        flight.setPlan(plan);
    } else {
        flight.setPosition(51, -1);
    }
    return flight;
}
```

This fits on one screen, but imagine that you have hundreds of lines of tests, and for each one you have to keep jumping to the bottom of the file to see what `setUpTestObject` will do in this specific instance.

Worse, what happens when someone else comes by and changes what `setUpTestObject` does, and it silently stops setting something important; behaviour you wanted to assert

After more than ten years writing tests, I can confidently say: **repeat yourself**.

Create a test object from scratch for each test.
Yes it is more lines, but you can look at the test and understand its purpose, inputs and assertions, without having to keep looking at other areas of the code.

### Always maintain backwards compatibility

So this one is probably the hardest of all.
Sometimes you figure out that the API you created is not getting you the results you wanted (maybe not driving a desired behaviour).
Or maybe the requirements have changed, and you need something different?

It's tempting to just bump to a new major version and remove the old way of doing things, delete the old code, and make the framework nice and shiny again.

A good example of this is when we wanted to add timing metrics to our dispatched events.
This was mostly to capture the origin time &mdash; the time the first event in a chain was created &mdash; which we needed to measure end-to-end latency.

Our original design was a simple dispatch method:

```java
void generateData() {
    MyPayload response = myDataSource.poll();
    dispatchHelper.dispatch(response);
}
```

However, the time between polling and the response might be significant; not large, but _significant_ for debugging issues.
We originally left gathering this time to each source of data, but we realised that we wanted a more standardised collection method.
So we redesigned the dispatch method:

```java
void generateData() {
    dispatchHelper.prepare(dispatcher -> {
        MyPayload response = myDataSource.poll();
        dispatcher.dispatch(response);
    });
}
```

This allows us to capture the start time when `prepare` is called.

But importantly, we only [deprecated](https://docs.oracle.com/en/java/javase/21/core/how-deprecate-apis.html) the original method; adding a _significant_ JavaDoc explanation of how to move to the new mechanism.
The older one still exists to this date.

But why?
Why wouldn't we force users to change their behaviour, not just prompt them with a `@Deprecated` annotation?

Well, engineers are like a light breeze when it comes to version updates.
Any resistance will result in them leaving the code on the older version, so they can 'deal with it later'.
Later is normally much longer than you would want (often never).
You want updates to be adopted automatically (via something like [Dependabot](https://github.com/dependabot)) and quickly, to address CVEs in dependencies.

Instead, we have adopted a pattern of adding features and letting the demand for those features drive updates.
Having the IDE underline the deprecated method in yellow seems to annoy most people enough to get them to update to newer signatures.

There are, of course, times when we have not been able to maintain backwards compatibility due to upstream changes, there have been times when we accidentally broke features we didn't intend for people to use (see [Anything you make public will be used](#anything-you-make-public-will-be-used)), and there have been times when we intentionally forced an API change.
But importantly we try to give users a low impact upgrade method to the new solution.

Maybe this is another [Make the right thing easy](#make-the-right-thing-easy), where 'the right thing' is 'keeping your dependencies up to date'.

### You can be too modular

This is something we learned after many years of maintaining the framework.

Because we had multiple application types, and we wanted to ensure that only the code required for your application was included, we split the application down into multiple modules:

Framework
: `core`
: `serialisation`
: `inbound`
: `sink`
: `outbound`
: `source`
: `transformer`
: `test-core`
: `test`
: `docker-test`

This meant that outbound dispatch code was not included in inbound only applications.
From a purists' perspective this is great, but it makes the code harder to work on when you are new to the project.

There are some clever advantages, like having two classes called `Dispatcher` where the API in the transformer version requires that you provide the upstream message, but the source one does not.
I'm not sure the advantages outweigh the added complexity.

If I were ever to start from scratch, I think I would take the Spring approach of a single dependency which has 'modes' of operation.

### Anything you make public will be used

This is probably obvious to some, but any API you make public, over a long enough time frame, will be leveraged by someone to build something.

Any behaviour, even if unintended, will be incorporated into production software.

This isn't limited to the code you write, the dependencies your dependency tree will also be used, and if one of your dependencies removes its usage of some library, your users will lose a transitive dependency.

That last one is pretty hard to defend against, but the first two you can mitigate.
Set class and method visibility to package or default visibility, where possible, and have higher than normal test coverage to cover as much behaviour as possible (we target 95%).

### You need lots of good tests

So 95% might sound absurdly high, because it is.

We did try to achieve close to 100% in the early days, but it's actually not possible due to things like default switch clauses for enums.
We strive for such a high number because it means the happy and unhappy paths of the framework are asserted, and thus maintained, through any updates.

I'm sure many of you reading (assuming anyone does read this) are saying things like "test coverage doesn't mean anything because you can write garbage tests", which I completely agree with.

High test coverage alone is not a useful metric, it needs to be paired with good engineering practices, principally a high quality code review.
A {{< term "PR" >}} (or {{< term "MR" >}}) on a framework should receive an extremely thorough review, because missing something has a high impact.

To measure the quality of tests, I leverage mutation tools like [PIT](https://pitest.org):

> Mutation testing is conceptually quite simple.
>
> Faults (or mutations) are automatically seeded into your code, then your tests are run. If your tests fail then the mutation is killed, if your tests pass then the mutation lived.
>
> The quality of your tests can be gauged from the percentage of mutations killed.

Yes, it effectively tests the quality of the tests.
We don't have this wired in to our build so that it fails it (yet), but I periodically use it to ensure that we are writing good tests (normally when a new contributor appears).

Additionally, I encourage engineers to write `GIVEN, WHEN, THEN` statements for their tests, so the intended behaviour is recorded; useful for preserving intent from eager refactoring:

```java
@Test
void testFlightWithoutPlan() {
    // GIVEN a flight without a plan
    Flight flight = new Flight();

    // WHEN calculating the length of the planned route
    LengthCalculator calculator = new LengthCalculator();
    Double length = calculator.calculate(flight);

    // THEN null is returned as there was no flight plan
    assertThat(length).isNull();
}
```

### Speculative features can be good and bad

Over the years I have occasionally, in times of inspiration, added features that I feel we will need in the near future.

Sometimes these features turn out to be useful, and sometimes a waste of time.

The best and most widely used speculative feature was support for Prometheus metrics.
We transitioned from StatsD to Prometheus last year, and having support already built into each service was helpful for the migration.

On the other hand, I integrated [Jaeger Tracing](https://www.jaegertracing.io/) into the framework using the [Opentracing](https://opentracing.io/) SDK.
But after so many breaking changes in the Opentracing API, and the fact none of our teams were leveraging it, we decided to remove support for it.

My lesson learned would be to wait until someone asks for a feature before building it, to maximise work not done.
This may seem obvious, but sometimes you get carried away on passion projects.

### No one will read the docs

This one is probably the most obvious.
Everyone _knows_ that developers don't read documentation.

However, after spending significant time writing upgrade notes and documentation over the years, I will continue to do so.

In a growing business there is a point where you can't explain changes via word of mouth, so the documentation becomes invaluable.
Having a well described upgrade path is a useful resource to point engineers toward.

## Fin

Thanks for reading!
