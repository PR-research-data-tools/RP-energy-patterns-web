# Interview Results for P1-P3

Answers on where to find each pattern:
|Pattern           | Comments                 |
| ---------------  | -------------------------|
|Dark UI Colors    |Is not implemeted in the customer portal. Generally look at available packages/libraries for style. And define style sheets (css, etc).|
|                  |No, we don't have a dark UI. We plan on doing so in the near future, bc everybody loves dark UI.|
|                  |Django allows for dark UI. Check libraries (Element Plus/Pinia) & provide toggle.|
|Dynamic Retry Delay|No, the only option would be to refresh the frontend, but we don't do that. If the initial request fails, we just assume that the backend is down.|
|                  |Generally in the frontend when a request fails, we reload the whole page. Look at 'life cycle hooks' (mount&fetch).|
|                  |No delays, only max retries for connecting to an api. Take a look at \[*some file*]|
|Avoid Extraenous Work|We use abstract loggers. For example in the \[django] admin view to be used in many different places.    |
|                  |Yes, we try to avoid doing unnecessary things.|
|                  |Implementing custom functions allows us to only compute values for a bill which are needed. It is sort of a lazy approach.|
|Race-to-idle      |We use RestfulAPI so we don't keep communication channels open.|
|                  |We use RestAPI (sending HTTP). There is a refresh token (that refreshes every minute) to be able to access APIs and stay logged in. This could be optimized (do fewer refreshes).|
|                  |When testing we use fixtures which have tear downs (possibly provided by django).|
|Open Only When Necessary|So our frontend is a single page application. It loads everything at once and there is a lot of data traffic to be able to render the page. When loading we do load some things that are not shown i.e. information for \[*some file*]. We don't load some of the dynamic things.|
|                  |I think this is also found in the life cycle hooks.|
|                  |-|
|Push Over Poll    |We only poll.|
|                  |Polling is done. It might be better to implement a WebSocket.|
|                  |We actually have an anti-pattern for this one: when a bill is being generated on the server, the frontend requests the state of the bill constantly.|
|Power Save Mode   |No.|
|                  |Definetly don't do that. We don't have options for the user to i.e. not load plots automatically.|
|                  |We don't have that.|
|Power Awareness   |No.|
|                  |This does not seem applicable to Web Applications.|
|                  |We don't have that.|
|Reduce Size       |Timeseries which are returned (and are very big) can be requested to only get summary by \[*some parameter*].|
|                  |I mean we don't send around unnecessary data, but there is no active reducing of http requests.|
|                  |We sometimes send big payloads from the backend (i.e., lots of meter data) which the frontend then has to deal with. Look at the meter data in \[*some file*].|
|Supress Logs      |We don't do enough logging! We could use maybe Google Analytics to find out more.|
|                  |We have introduced only few 'devlopment logs'. During debugging the frontend use chrome dev tools. Check Docker container console. On production for the backend there are files: \[*some files*].|
|                  |Current log level = info (changed from warning). This is the minimum. Look at \[*some file*].|
|Batch Operations  |We use batch.create() during testing. Also Redis jobs are used for batching.|
|                  |In the frontend look for promises. promise.all() for example collects a batch and triggers them all at once.|
|                  |No examples for pattern or anti-patterns come to mind. We use a single application therefore there is no need to talk to the server all the time.|
|Cache            |Yes, this has been implemented recently by a colleague. All the requests that come back from an API get cached.|
|                  |We use the vue store for caching. To avoid refetching and recalculating.|
|                  |All custom functions and most API calls are cached. It is signified by @memoize.|
|Decrease Rate    |We don’t have any sensors in the customer portal. No sensors, no sync rates.|
|                  |Not done.|
|                  |There is a refresh token \[to stay logged in]. Look in the dev tools when frontend is running.|
|User Knows Best  |-|
|                 |Not done.|
|                 |There is no option for users to not show plots in frontend.|
|Inform Users     |-|
|                  |No.|
|                  |We don’t do that at the moment.|
|Enough Resolution|Does not seem applicable to our project. Because we use Highcharts|
|                |Responses from API have high resolution i.e., lots of data usually.|
|                |Meters always have 15 min resolutions. This is because of legal reasons.|
|Kill Abnormal Tasks|Not given. We use timeouts during the whole billing process, but no means for the user to cancel.|
|                |Can be done by Docker. We can shut down and restart containers if things break.|
|                |You can delete bills before they are done.|
|No Screen Interaction|This is not applicable to our Portal. It does not make sense for our purposes.|
|                |-|
|                |No.|
|Avoid Extraneous Graphics and Animations|Nothing comes to mind. Because we use Highcharts for plots and we don’t use other animations.|
|              |Icons/pics very high resolution. Different types of icons for different screen size / device / usage have to be provided for progressive web applications. They can be found in \[*some folder*].|
|              |No animations used. Only Highcharts.|
|Manual Sync, On Demand|Not appearing at the moment. Could make sense for the plots in the frontend.|
|              |We only fetch new data if requested by the users. Look at \[*some file*].|
|              |Look at \[*some file*].|
