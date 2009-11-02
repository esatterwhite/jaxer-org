<?php $sidebar = true; ?>
<?php $active = 'tutorials';?>
<?php $title = 'Your First Complex Jaxer Application - To Do Manager'; ?>
<?php include('../includes/header.php'); ?>
  <h3>
  This sample ships with code updated for Jaxer 1.0 and Aptana Studio 1.2 and is a good sources of information but the tutorial has not yet been revised to match.
  </h3>

  		<h2>Contents</h2>
  		<ul>
  			<li><a href="#Introduction">Introduction</a><ul>
  				<li><a href="#Benefits_of_using_Jaxer">Benefits of using Jaxer</a></li>
  				<li><a href="#Architecture">Architecture</a></li></ul></li>
  			<li><a href="#Running_code_on_Jaxer">Running code on Jaxer</a><ul>
  				<li><a href="#Programmatic_runat_configuration">Programmatic runat configuration</a></li>
  				<li><a href="#Recommended_style">Recommended style</a></li>
  				<li><a href="#Examples">Examples</a></li>
  				<li><a href="#Alternate_Syntax">Alternate Syntax</a></li></ul></li>
  			<li><a href="#Jaxer_by_example:_Simple_.22Tasks.22_application_tutorial">Jaxer by example: Simple "Tasks" application tutorial</a><ul>
  				<li><a href="#Viewing_the_sample_application">Viewing the sample application</a></li>
  				<li><a href="#Creating_the_client-side_web_page">Creating the client-side web page</a></li>
  				<li><a href="#Scripting_the_client-side_page">Scripting the client-side page</a></li>
  				<li><a href="#Adding_server-side_functionality_to_tasks">Adding server-side functionality to tasks</a></li></ul></li>
  			<li><a href="#Complete_Code">Complete Code</a></li>					
  		</ul>

  		<a name="Introduction"></a>
  		<h2>Introduction</h2>
          <p>
              Rich, "Ajax-style" web sites and applications offer 
  			tremendous advantages over both static web sites and 
  			desktop applications. But they can be difficult to 
  			develop, maintain, and expand. Many of the difficulties 
  			on the client side are alleviated by Ajax libraries such 
  			as jQuery, EXT, and Dojo, and by development environments 
  			such as Aptana Studio. Jaxer, the Aptana server, completes 
  			the picture by offering a powerful "Ajax server." With Jaxer, 
  			you can develop your entire site or application using only 
  			standards-based DHTML, JavaScript, and CSS. You can populate 
  			the HTML DOM on the server before the page is served using 
  			the same techniques and libraries you would use on the client; 
  			call server-side JavaScript functions directly from client-side 
  			JavaScript; validate your data with the same code on both the 
  			server and the client; and do it all in a completely 
  			standards-based, flexible, open-source environment.
          </p>

          <a name="Benefits_of_using_Jaxer"></a>
          <h3>Benefits of using Jaxer</h3>
          <p>
              Let's take a closer look at what it takes to put together a modern web site or application.
          </p>
          <p>
              <b>Client-side paradigms</b>
          </p>
          <p>
              The key to developing modern, richly interactive web sites and applications is to start with the desired user experience and interface. Web application developers need to determine how information will be presented to the user and how will the user interact with it. Once a developer sketches out the basic information flow, several other high-level decisions become apparent:
          </p>
          <ul>
              <li>
                  Will this be a single-page app or will there be page transitions? 
              </li>
              <li>
                  How much data will be available at any given time?
              </li>
              <li>
                  How can the user control this data?
              </li>
          </ul>
          <p>
              After defining the user interface, a developer can create a mockup to walk through the design. This becomes imperative for web applications with rich interfaces, which require dynamic HTML mockups with working controls and realistic data. Increasingly, a developer will use one or more "Ajax libraries" to create a rich UI, styled with CSS. As a developer refines these client-side mock-ups, the web page that the user will see takes shape.
          </p>
          <p>
              <b>Server-side development paradigms</b>
          </p>


          <p>
              Developing a client-side web page is only part of the work involved in developing a rich internet application, however.  Developers encounter a new set of questions as they complete the development of their application:
          </p>
          <ul>
              <li>
                  Where does the data for the client come from? 
              </li>
              <li>
                  How will changes to that data be persisted? 
              </li>
              <li>
                  How will multiple users share data?
              </li>
          </ul>
          <p>
              Solving these issues requires a whole new set of technologies: the server side. For example, a server using PHP, Java, or Ruby, and often a templating framework, emits the HTML and the JavaScript needed for the client as one or more documents. The data needed by the client is then packaged into the page, usually by the templating framework writing JavaScript-format text. For rich web controls such as grids or calendars, the server-side templates cannot always emit exactly the HTML needed by the client-side Ajax library, so often the server will only emit an empty HTML container, and the client-side Ajax library must return to the server to fetch the data it needs to create the HTML for the control.
          </p>
          <p>
              Client communication back to the server presents more issues. Ajax 
  			libraries simplify sending the data from the client, but then 
  			the server side must be set up to accept a large variety of 
  			requests and return the data in some format that the client can 
  			then read. Frequently, a templating framework writes (and escapes) 
  			PHP data into XML or JSON for transmission back to the client. 
  			Data validation on both the client and the server present even more 
  			issues,  for example, how do you keep them in sync?
          </p>
          <p>
              <b>Eliminating the gap between client and server</b>
          </p>
          <p>
              Jaxer eliminates the complexity of using different technologies for client and server. With Jaxer, developers can use a single set of technologies—the ones closest to their users: HTML, JavaScript, and CSS. 
          </p>
          <p>
              As always, the page the user will see starts on the server, but now this page can just be the same static page that was mocked up in the design phase. As a developer, you can designate some JavaScript to run on the server before the page is sent to the client, such as code that accesses a database to fill up a grid. You can also designate some of the JavaScript to remain on the server but be accessible from the client, such as code to update the database with new data from the client, or retrieve database data for refreshing the client. In this case, when the user interacts with the page to fire events, these events trigger client-side JavaScript that can directly call the functions you designated to stay behind on the server.
          </p>
          <p>
              Jaxer enables you to use Ajax-style development end-to-end. You can even use your favorite Ajax libraries for all of your development! This provides you with several key development benefits:
          </p>
          <ul>
              <li>
                  The same code can validate data on both the client (for immediate user feedback) and on the server (for security), so validations never get out of sync. 
              </li>
              <li>
                  The same code can prepare both the HTML DOM server side (for better perceived responsiveness) and modify it client-side (when the user changes the data or it’s refreshed from the server).
              </li>
              <li>
                  Using the same code on both the client and the server, developers have fewer technologies to learn and stay on top of, and fewer parts of the application or site to maintain.
              </li>
          </ul>

          <a name="Architecture"></a>
          <h3>Architecture</h3>
          <p>
              Jaxer is pre-configured for use as a plug-in to the Apache 2.x web server. Future versions will support more configurations. To provide world-class, standards-compliant JavaScript and DOM capabilities server-side, Jaxer is built on the Mozilla engine, which is the same engine used in the popular Firefox browser. Jaxer is layered into Apache as an input and output filter so that you can also use Jaxer to modify dynamic pages created by other languages, such as PHP or Ruby.
          </p>
          <p>
              <b>Jaxer Core vs. Framework</b>
          </p>
          <p>
              Jaxer itself is a combination of C/C++ "Core" code and a server-side JavaScript "Framework." The Core provides the JavaScript parser and runtime, HTML parser and DOM engine, and an event architecture that calls the Framework as the document is being processed on the server. The Framework provides the Jaxer logic itself, for example deciding which code to run on the server and which on the client, creating proxies on the client for callable server-side functions, serializing and deserializing data, and so on.
          </p>
          <p>
              Because the Framework is written in JavaScript, it is easily extensible by Aptana or other developers. Jaxer is an open-source, free, and extensible platform for end-to-end Ajax development and for building rich presentation layers on top of existing back-end platforms.
          </p>
          <p>
              <b>Jaxer page lifecycle</b>
          </p>
          <p>
              Let's examine the lifecycle of a typical web page built with Jaxer:
          </p>
          <ol>
              <li>
                  The HTML document starts life on the server, either as a static HTML file read from disk, or as a dynamic page generated by PHP, Ruby, Java, etc.
              </li>
              <li>
                  Jaxer receives the document as an output (post-process) filter from Apache, and starts to parse and execute it, just as a browser would. Jaxer creates and populates the DOM, executes the JavaScript code designated to run on the server, and so on until the entire document is consumed.
              </li>
              <li>
                  The result is a DOM modified by the Framework and by the developer: in particular, proxies automatically replace server-side client-callable functions. Some important side effects include storing designated JavaScript functions as callbacks and persisting session-type data.
              </li>
              <li>
                  The new DOM is serialized as an HTML document and streamed out to the client as usual.
              </li>
              <li>
                  The client receives the HTML document and the processing continues, recreating the DOM from HTML and this time executing the client-side JavaScript left in the page.
              </li>
              <li>
                  When one of the client-side proxy functions is called, its parameters are automatically serialized into a JSON (JavaScript Object Notation) format, and an XMLHttpRequest is sent to the server to invoke the original function with these parameters.
              </li>
              <li>
                  When the server receives this special request, the parameters are deserialized, the function to be invoked is restored and called with these parameters, and the results (or any exception) are serialized back into JSON.
              </li>
              <li>
                  The data is returned to the client, where it is deserialized and returned as the result of the proxy (or a corresponding client-side exception is thrown).
              </li>
          </ol>
          <p>
              On the server side, the developer's JavaScript environment is enhanced by the Jaxer Framework, which provides access to the database (MySQL only at this time), file system, network (coming soon), the HTTP Request and Response data, and in the future also external server-side platforms such as Java, PHP, and Ruby.
          </p>

          <a name="Running_code_on_Jaxer"></a>
          <h2>Running code on Jaxer</h2>
          <p>
              To define and/or execute any code server-side, add a 
              <tt>
                  runat
              </tt>
              attribute to a 
              <tt>
                  &lt;script&gt;
              </tt>
              block. This attribute has several possible values, and they determine where the code will execute (whenever this page is served) and what other actions will automatically take place:
          </p>
          <table>
              <tbody>
                  <tr>
                      <th>
                          value
                      </th>
                      <th>
                          description
                      </th>
                  </tr>
                  <tr>
                      <td>
                          client
                      </td>
                      <td>
                          <p>
                              The functions and code contained in the script block will run in the client browser only. This functions exactly as a regular script block. This is the default value of the 
                              <tt>
                                  runat
                              </tt>
                              attribute, so usually you'll omit it for 
                              <tt>
                                  script
                              </tt>
                              blocks intended for the client. Its main use is to override the 
                              <tt>
                                  runat
                              </tt>
                              attribute of a specific function within a server-side 
                              <tt>
                                  script
                              </tt>
                              block. <i>Note: if a 
                                  <tt>
                                      script
                                  </tt>
                                  block has 
                                  <tt>
                                      runat = "client"
                                  </tt>
                                  (or no 
                                  <tt>
                                      runat
                                  </tt>
                                  attribute), it will not run at all server-side, so you cannot override the 
                                  <tt>
                                      runat
                                  </tt>
                                  behaviors of individual functions from within this block.
                              </i>
                          </p>
                      </td>
                  </tr>
                  <tr>
                      <td>
                          server
                      </td>
                      <td>
                          <p>
                              The functions and code contained in the script will run on the server only. 
                              Any functions defined within the script block will be cached in association with this page.  
                              These functions are not directly callable from the client, but they can be called during callback processing by other server-side functions. 
                              These script blocks will not be presented to the client browser.
                          </p>
                      </td>
                  </tr>
                  <tr>
                      <td>
                          both
                      </td>
                      <td>
                          <p>
                              The functions and code contained in the script will run on both the client and the server. 
                              Any functions defined within the script block will be cached in association with this page.  
                              The server-side functions are not directly callable from the client, but they can be called during callback processing by other server-side functions. 
                          </p>
                      </td>
                  </tr>
              </tbody>
          </table>
          <p>
              Although most use cases will be covered by the basic attributes shown above, You can use the following 
              <tt>
                  runat
              </tt>
              values on 
              <tt>
                  &lt;script&gt;
              </tt>tags:
          </p>
          <table>
              <tbody>
                  <tr>
                      <th>
                          value
                      </th>
                      <th>
                          description
                      </th>
                  </tr>
                  <tr>
                      <td>
                          server-proxy
                      </td>
                      <td>
                          Same as the basic 'server' target except ALL the functions will be proxied by default
                      </td>
                  </tr>
                  <tr>
                      <td>
                          server-nocache
                      </td>
                      <td>
                          Same as the basic 'server' target except NONE of the functions will be cached by default
                      </td>
                  </tr>
                  <tr>
                      <td>
                          both-proxy
                      </td>
                      <td>
                          Same as the basic 'both' target except ALL the functions will be proxied by default
                      </td>
                  </tr>
                  <tr>
                      <td>
                          both-nocache
                      </td>
                      <td>
                          Same as the basic 'both' target except NONE of the functions will be cached by default
                      </td>
                  </tr>
              </tbody>
          </table>

          <a name="Programmatic_runat_configuration"></a>
          <h3>Programmatic runat configuration</h3>
          <p>
              Jaxer is aware of some special function object properties that can be declared on individual function objects to control how they are managed. When these are specified the property value will override the containing script block 
              <tt>
                  runat
              </tt>
              setting for the individual function. This allows more granular control and prevents the need to break scripts out into separate files depending on their 
              <tt>
                  runat
              </tt>
              target. 
          </p>
          <table>
              <tbody>
                  <tr>
                      <th>
                          property
                      </th>
                      <th>
                          description
                      </th>
                  </tr>
                  <tr>
                      <td>
                          proxy
                      </td>
                      <td>
                          <p>
                              Server-side functions can be declared to be proxied so they are callable from the client side. This is achieved by specifying a 
                              <tt>
                                  proxy
                              </tt>
                              property on the function object. The possible values for this property are 
                              <tt>
                                  true
                              </tt>
                              or 
                              <tt>
                                  false
                              </tt>. This is only required for enabling the proxying of the function. By default, in a 
                              <tt>
                                  &lt;script runat="server"&gt;
                              </tt>
                              block, the functions are not proxied. Note that if a function is not proxied, it isn't just that proxies are not inserted into the client to facilitate calling it: it's actually marked as not callable on the server, so hacking the client to try to call the function on the server will not work.
                          </p>
                      </td>
                  </tr>
                  <tr>
                      <td>
                          runat
                      </td>
                      <td>
                          <p>
                              Takes the same values as the 
                              <tt>

                                  &lt;script&gt;
                              </tt>
                              tag 
                              <tt>
                                  runat
                              </tt>
                              attributes.
                          </p>
                      </td>
                  </tr>
              </tbody>
          </table>

          <a name="Recommended_style"></a>
          <h3>Recommended style</h3>
          <p>
              The following illustrates one simple way of using the 
              <tt>
                  runat
              </tt>
              and 
              <tt>
                  proxy
              </tt>
              options 
              in a typical code scenario. We choose to group all the server-side code in one 
              <tt>
                  script
              </tt>
              block, and explicitly designate a subset of function to be proxied. Then all client-side code 
              goes in a different 
              <tt>
                  script
              </tt>
              block (where there isn't even the option of programatically 
              changing it by setting a different 
              <tt>
                  runat
              </tt>
              or 
              <tt>
                  proxy
              </tt>
              value). 
              Of course you may choose a different way of organizing your code if that makes more sense.
              And for large amounts of code, it may also make sense to extract the code into (reusable)
              external JavaScript files.
          </p>
  <textarea name="code" class="html"><script type="text/javascript" runat="server"> 
  	function setPassword(username, newPassword)
  	{
  		// put code in here to directly set the password of a given username
  		// this code should not be callable from the client
  	} 

  	function changePassword(username, oldPassword, newPassword){
  		// put code in here to first verify the submitted password,
  		// and then -- if successful -- call setPassword to actually make changes
  		// this code should be callable from the client
  	}
  	changePassword.proxy = true; 
  </script> 

  <script type="text/javascript"> 
  	function submitPassword()
  	{
  		// put client-side code here to grab the username and old and new passwords
  		// and call changePassword on the server
  	} 
  </script>
  </textarea>        <a name="Examples"></a>
          <h3>Examples</h3>
          <p>
              The <b>_login.js</b>
              file referenced in the example above contains some functions that explicitly override the 
              <tt>
                  runat='server'
              </tt>
              directive specified on the script tag used to load the file.
          </p>
          <p>
              <b>Proxy example</b>
          </p>
          <p>
              In the following snippet, the function will proxied:
          </p>
  <textarea name="code" class="javascript">function checkCredentials(username, password)
  {
  	var rs = Jaxer.DB.execute("SELECT * FROM users WHERE username = ? AND password = ?",
  		[username, password]);
  	if (rs.rows.length == 0)
  	{
  		return "";
  	}
  	var user = rs.rows[0];
  	makeAuthenticated(user);
  	return user.username;
  }
  checkCredentials.proxy = true;        <p>
   </textarea>           <b>Client-side example</b>
          </p>
          <p>
              In the following snippet the function will run client side. 
          </p>
  <textarea name="code" class="javascript"> function login()
  {
  	var username = $('username').value;
  	var password = $('password').value;
  	var username = checkCredentials(username, password);
  	if (username != "")
  	{
  		fromTemplate('loginComponent', 'loginAuthenticated');
  		setTimeout("$('authenticatedUsername').innerHTML = '" + username + "'", 0);
  		changeAuthentication(true);
  	}
  	else
  	{
  		$('loginMessage').innerHTML = "Sorry, try again";
  	}
  }
  login.runat = "client";
  </textarea>
          <a name="Alternate_Syntax"></a>
          <h3>Alternate Syntax</h3>
          <p>
              Jaxer provides a useful convenience object inside the Jaxer namespace to allow the proxy functions to be declared in a single group within your JavaScript code:
          </p>
          <div class="csh">
              <pre class="javascript"><ol><li style="border: 0px solid green; margin: -1px; padding: 0pt;"><div style="font-family: 'Courier New',Courier,monospace; font-weight: normal;">Jaxer.<span style="color: rgb(0, 102, 0);">proxies</span> = <span style="color: rgb(102, 204, 102);">[</span>myFunc1, myFunc2, <span style="color: rgb(51, 102, 204);">"myFunction"</span><span style="color: rgb(102, 204, 102);">]</span>; </div></li><li style="border: 0px solid green; margin: -1px; padding: 0pt;"><div style="font-family: 'Courier New',Courier,monospace; font-weight: normal;"><span style="color: rgb(0, 153, 0); font-style: italic;">// ...</span></div></li><li style="border: 0px solid green; margin: -1px; padding: 0pt;"><div style="font-family: 'Courier New',Courier,monospace; font-weight: normal;">Jaxer.<span style="color: rgb(0, 102, 0);">proxies</span> = Aptana.<span style="color: rgb(0, 102, 0);">proxies</span> .<span style="color: rgb(0, 102, 0);">push</span><span style="color: rgb(102, 204, 102);">[</span>myFunc3, <span style="color: rgb(51, 102, 204);">"myFunction4"</span><span style="color: rgb(102, 204, 102);">]</span>;</div></li></ol></pre>
          </div>
          <p>
              This code must be presented in such a way that it is executed by the server prior to DOM serialization. You can also use this to remove the proxied functions by setting the value to null.
          </p>
          <p>
              <b>Note:</b>
              <tt>
                  Jaxer.proxies
              </tt>
              is NOT a complete collection of the functions being proxied by the server it is just a convenient way to express the 
              <tt>
                  myFunc.proxy=true;
              </tt>
              syntax for multiple function references. 
          </p>
          <p>
              The 
              <tt>
                  runat
              </tt>
              attribute applies to everything within the 
              <tt>
                  &lt;script&gt;
              </tt>
              block. Individual functions within the 
              <tt>
                  &lt;script&gt;
              </tt>
              block can be changed to a different 
              <tt>
                  runat
              </tt>
              value by adding a 
              <tt>
                  runat
              </tt>/
              <tt>
                  proxy
              </tt>
              property to them and setting it to the appropriate (string) value: for example, 
              <tt>
                  myFunction.runat = "both"
              </tt>. The one exception is for 
              <tt>
                  &lt;script&gt;
              </tt>
              blocks that don't have a 
              <tt>
                  runat
              </tt>
              attribute (or have 
              <tt>
                  runat="client"
              </tt>): since such 
              <tt>
                  &lt;script&gt;
              </tt>
              blocks are not executed at all on the server, setting 
              <tt>
                  runat
              </tt>
              properties within those 
              <tt>
                  &lt;script&gt;
              </tt>
              blocks will not take place on the server, so the behavior of functions within them cannot be changed from within them.
          </p>

          <a name="Jaxer_by_example:_Simple_.22Tasks.22_application_tutorial"></a>
          <h2>Jaxer by example: Simple "Tasks" application tutorial</h2>
          <p>
              This tutorial describes how to create a simple, one-page Ajax-style application to keep track of a list of tasks. The user can create new tasks, check off and delete existing tasks, and all the data should persist and be accessible from any browser. The functionality in this example is extremely simple to focus on the basics (e.g. no logging in step). Although you'll probably use one of the many popular Ajax libraries, such as jQuery, EXT, Dojo, or YUI, in building your own applications, this simple tutorial assumes no specific Ajax library use, and only uses the JavaScript built into any modern browser and keeps all CSS, JavaScript, and HTML in a single document.
          </p>

          <a name="Viewing_the_sample_application"></a>
          <h3>Viewing the sample application</h3>
          <p>
              Your Jaxer installation (whether as a standalone Jaxer Package or in Aptana Studio) includes this simple task application.
          </p>
          <p>
              To access the tasks application from within Aptana Studio:
          </p>
          <p>
          </p>
          <ol>
              <li>
                  In the Samples View, expand the <b>Aptana Jaxer</b>
                  folder.
              </li>
              <li>
                  Select the <b>tasks</b>
                  example.
              </li>
              <li>
                  Click either the <b>Preview Sample</b>
                  button <img src="<?php print WEB_ROOT; ?>/images/iconPreviewSample.png" /> to do a quick preview of the sample, or click the <b>Import Sample</b>
                  button <img src="<?php print WEB_ROOT; ?>/images/iconImportSample.png" /> to import the sample as a project into your workspace.
              </li>
          </ol> To access the tasks application from a standalone Jaxer Package installation:
          <ol>
              <li>
                  Navigate to your Jaxer installation folder, and double-click the <b>StartServers.bat</b>
                  file.
              </li>
              <li>
                  In your web browser, navigate to the following URL: <a href="http://localhost:8081/aptana/" class="external free" title="http://localhost:8081/aptana/" rel="nofollow">http://localhost:8081/aptana/</a>
              </li>
              <li>
                  From the column on the left, click the <b>Apps and Tools</b>
                  link.
              </li>
              <li>
                  Click the <b>Tasks</b>
                  link.
              </li>
              <p>
              </p>
          </ol>

          <a name="Creating_the_client-side_web_page"></a>
          <h3>Creating the client-side web page</h3>
          <p>
              This section describes how to create your own tasks application from scratch.
          </p>
          <p>
              To create the client-side:
          </p>
          <p>
          </p>
          <ol>
              <li>
                  Create a basic HTML page. The example below contains several example tasks:
  <textarea name="code" class="html"><html>
  <head>
  	<title>Tasks</title>
  	</head>
  	<body>
  		<h2>Tasks To Do</h2>

  		<div class="new-task">
  			New:
  			<input type="text" id="txt_new" size="60">

  			<input type="button" id="btn_new" value="add">
  		</div>

  		  <div id="tasks" class="tasks">
  		   <div id="task_0" class="task">

  			<input type="checkbox" title="Done">
  			<input type="text" size="60" title="description"

  				 value="Bring home some milk">
  		   </div>
  	     	   <div id="task_1" class="task">

  			<input type="checkbox" title="Done">
  			<input type="text" size="60" title="description"

  				 value="Prepare presentation">
  		    </div>
  		    <div id="task_2" class="task">

  			<input type="checkbox" title="Done">
  			<input type="text" size="60" title="description"

  				 value="Make car reservations">
  		    </div>
  		    <div id="task_3" class="task">

  			<input type="checkbox" title="Done">
  			<input type="text" size="60" title="description"

  				 value="File taxes">
  		    </div>
  		</div>
  	</body>
  </html>
  </textarea>            </li>
              <li>
                  Preview the page in a browser, you should see something similar to the example below:
                  <p>
                      <img src="<?php print WEB_ROOT; ?>/images/taskcap.png"  />
                  </p>
              </li>
              <li>
                  To add formatting, add a style block at the bottom of the 
                  <tt>
                      &lt;head&gt;
                  </tt>
                  section:
  <textarea name="code" class="html">		<style type="text/css">
  			.tasks { 
  				background-color: #f0f0ff; 
  				padding: 8px;
  			}

  			.new-task {
  				padding: 4px 0 4px 0; 
  				border-bottom: 3px solid #B5B5DF;
  			}

  			.task { 
  				padding: 4px; 
  			}
  		</style>
  </textarea>            </li>
              <li>
                  Preview the page again to see the styles added:
                  <p>
                      <img src="<?php print WEB_ROOT; ?>/images/toDo2.png" />
                  </p>
              </li>
              <p>
              </p>
          </ol>
          <p>
              This web page is starting to look nice, but it does not have any functionality yet. Next, you will delete the sample data and add some event handlers and a bit of JavaScript.
          </p>

          <a name="Scripting_the_client-side_page"></a>
          <h3>Scripting the client-side page</h3>
          <p>
              To add a simple client-side script to the page:
          </p>
          <p>
          </p>
          <ol>
              <li>
                  Add a helper function to ease DOM access. Add the following script block to the 
                  <tt>
                      &lt;head&gt;
                  </tt>
                  element:
                  <p>
                  </p>
   <textarea name="code" class="javascript">			/*
  			 * Easy access to a named element in the DOM
  			 */
  			function $(id) 
  			{ 
  				return document.getElementById(id); 
  			}
  </textarea>                <p>
                      When the user types a description into the top textbox and clicks add, a new task line should be created at the top of the list.
                  </p>
              </li>
              <li>
                  Add an 
                  <tt>
                      onclick
                  </tt>
                  event handler to the button to grab the value of the textbox and call a JavaScript function that will add the task.
  <textarea name="code" class="html"><input type="button" value="add" onclick="addTaskToUI($('txt_new').value)">     </textarea>       
  </li>
              <li>
                  Remove the rows of sample data from the HTML. The new function 
                  <tt>
                      addTask(description, id)
                  </tt>
                  will insert the new task into the DOM. For future use, allow the id to be specified or else be auto-generated. Add this to the above 
                  <tt>
                      &lt;script&gt;
                  </tt>
                  block:
  <textarea name="code" class="javascript">		<script type="text/javascript" runat="both">
  			function addTaskToUI(description, id)
  			{
  				var newId = id || Math.ceil(1000000000 * Math.random());
  				var div = document.createElement("div");
  				div.id = "task_" + newId;
  				div.className = "task";

  				var checkbox = document.createElement("input");
  				checkbox.setAttribute("type", "checkbox");
  				checkbox.setAttribute("title", "done");
  				checkbox.setAttribute("id", "checkbox_" + newId);
  				div.appendChild(checkbox);

  				var input = document.createElement("input");
  				input.setAttribute("type", "text");
  				input.setAttribute("size", "60");
  				input.setAttribute("title", "description");
  				input.setAttribute("id", "input_" + newId);
  				input.value = description;
  				Jaxer.setEvent(input, "onchange", "saveTaskInDB(" + newId + ", this.value)");
  				div.appendChild(input);

  				$("tasks").insertBefore(div, $("tasks").firstChild);

  				if (!Jaxer.isOnServer)
  				{
  					saveTaskInDB(newId, description);
  				}
  			}
  		</script>
  </textarea>
                  <p>
                      <b>Note:</b>
                      This 
                      <tt>
                          addTask
                      </tt>
                      uses pure DOM manipulation. You could instead create the HTML as a string or copy a hidden HTML block (acting as a template) and convert it into the new HTML fragment. Usually you would use your favorite Ajax library to achieve this quickly.
                  </p>
              </li>
              <li>
                  Your application now has some basic functionality. Preview it in your browser again.
                  <p>
                      You are now ready to add the last bit of functionality. When you check off a task as done, it should disappear from the list.
                  </p>
              </li>
              <li>
                  Add another function to the script block, 
                  <tt>
                      completeTask(taskId)
                  </tt>, to delete the task and its contents from the DOM, and add a line to 
                  <tt>
                      addTask
                  </tt>
                  that will add a call to 
                  <tt>
                      completeTask
                  </tt>
                  from the checkbox's 
                  <tt>
                      onclick
                  </tt>
                  handler:
  <textarea name="code" class="javascript">		<script type="text/javascript" runat="both">
  			function addTaskToUI(description, id)
  			{
  				var newId = id || Math.ceil(1000000000 * Math.random());
  				var div = document.createElement("div");
  				div.id = "task_" + newId;
  				div.className = "task";

  				var checkbox = document.createElement("input");
  				checkbox.setAttribute("type", "checkbox");
  				checkbox.setAttribute("title", "done");
  				checkbox.setAttribute("id", "checkbox_" + newId);
  				Jaxer.setEvent(checkbox, "onclick", "completeTask(" + newId + ")");
  				div.appendChild(checkbox);

  				var input = document.createElement("input");
  				input.setAttribute("type", "text");
  				input.setAttribute("size", "60");
  				input.setAttribute("title", "description");
  				input.setAttribute("id", "input_" + newId);
  				input.value = description;

  				div.appendChild(input);

  				$("tasks").insertBefore(div, $("tasks").firstChild);

  				if (!Jaxer.isOnServer)
  				{
  					saveTaskInDB(newId, description);
  				}
  			}
  		</script>
  </textarea>
             </li>
              <p>
              </p>
          </ol>
          <p>
              You can now add tasks, complete and delete them, and modify their descriptions; however you cannot save or retrieve data yet.
          </p>
          <p>
              <b>Note</b>: to add the 
              <tt>
                  onclick
              </tt>
              event handler programatically to the checkbox, we used the 
              <tt>
                  Jaxer.setEvent(domElement, eventName, handler)
              </tt>
              function. There are multiple ways to add event handlers to a DOM element programatically. As you'll soon see, we'll need 
              <tt>
                  addTask
              </tt>
              to work both server-side and client-side. On the server we'll need to add the event handler to the DOM, changing the HTML that's then sent to the client. If we would have used 
              <tt>
                  checkbox.onclick = "completeTask(" + newId + ")"
              </tt>
              that would have added the event handler without changing the DOM, so the handler would not have made it to the client. The 
              <tt>
                  Jaxer.setEvent
              </tt>
              function "does the right thing" on both server and client, modifying the DOM on the former and directly setting the 
              <tt>
                  onclick
              </tt>
              property of the checkbox on the latter. <i>The key lesson to remember: <b>only DOM modifications make it from the server to the client</b>.</i>
          </p>

          <a name="Adding_server-side_functionality_to_tasks"></a>
          <h3>Adding server-side functionality to tasks</h3>
          <p>
              This example uses MySQL to save and retrieve tasks data. (Make that 
  			sure you have adjusted config.js in your Jaxer installation 
  			directory before continuing. See the installation and configuration 
  			instructions.) The Jaxer Framework gives access to MySQL. The 
  			Framework is accessible within the Jaxer namespace (JavaScript 
  			global object) server-side, and a small part of it is also inserted 
  			into the Jaxer namespace client-side. The Framework, to minimize 
  			name collisions, defines no other global variables.
          </p>
          <p>
              To add server-side functionality to save and retrieve your task data:
          </p>
          <p>
          </p>
          <ol>
              <li>
                  Create the database table to store the tasks, if it isn't already there. Add a 
                  <tt>
                      runat="server"
                  </tt>
                  attribute to your 
                  <tt>
                      &lt;script&gt;
                  </tt>
                  block (See the section about <a href="/wiki/index.php/Running_code_on_Jaxer" title="Running code on Jaxer">Running code on Jaxer</a>
                  to learn more about runat attributes) and add the following code:
  <textarea name="code" class="javascript">			/*
  			 * The SQL to create the database table we'll use to store the tasks
  			 */
  			var sql = "CREATE TABLE IF NOT EXISTS tasks " +
  				"( id INTEGER NOT NULL" +
  				", description VARCHAR(255)" +
  				", created DATETIME NOT NULL" +
  				")";

  			// Execute the sql statement against the default Jaxer database
  			Jaxer.DB.execute(sql);
  </textarea>                <p>
                      <b>Note:</b>
                      When you call 
                      <tt>
                          Jaxer.DB.execute(…)
                      </tt>, you are using our default connection settings as defined in <b>config.js</b>, e.g. using the "demos" database specified in the default <b>config.js</b>
                      that ships with Jaxer. If this database does not yet exist, it will be created automatically for you when Jaxer serves the first page.
                  </p>
              </li>
              <li>
                  Add code to populate the DOM on the server with any saved tasks, before the page is sent to the client. This code executes after the DOM has been loaded into the server, so add it into a 
                  <tt>
                      window.onserverload
                  </tt>
                  event handler, similar to using a 
                  <tt>
                      window.onload
                  </tt>
                  handler. Use a SQL SELECT query to read the tasks from the database into a 
                  <tt>
                      resultSet
                  </tt>
                  object, and iterate over its rows. For each task row, add a task to the DOM using the same code as on the client:
  <textarea name="code" class="javascript">			/*
  			 * Set the 'onserverload' property to call our function once the page has been fully
  			 * loaded server-side. We could have also set this attribute on the &ltbody> tag of our
  			 * page and had it call a function by name.
  			 */
  			window.onserverload = function()
  			{
  				var resultSet = Jaxer.DB.execute("SELECT * FROM tasks ORDER BY created");
  				for (var i=0; i&ltresultSet.rows.length; i++)
  				{
  					var task = resultSet.rows[i];
  					addTaskToUI(task.description, task.id);
  				}
  			}
  </textarea>                <p>
                      <b>Note:</b>
                      Usually 
                      <tt>
                          addTask
                      </tt>
                      would use some 3rd-party Ajax library to create and add the DOM fragment for the task. Because both the DOM and JavaScript are on the server, you can use exactly the same 
                      <tt>
                          addTask
                      </tt>
                      with the same Ajax library also on the server-side, and ensure that the HTML emitted from the server is exactly what the client needs. Just set 
                      <tt>
                          addTask.runat="both"
                      </tt>
                      (or put it in a 
                      <tt>
                          &lt;script runat="both"&gt;
                      </tt>
                      block).
                  </p>
              </li>
              <li>
                  Add a server-side function to save a task, updating or inserting it as necessary, and make it callable from the client:
  <textarea name="code" class="javascript">			/*
  			 * Save a task directly into the database
  			 */
  			function saveTaskInDB(id, description)
  			{
  				var resultSet = Jaxer.DB.execute("SELECT * FROM tasks WHERE id = ?", [id]);
  				if (resultSet.rows.length > 0) // task already exists
  				{
  					Jaxer.DB.execute("UPDATE tasks SET description = ? WHERE id = ?",
  						[description, id]);
  				}
  				else // insert new task
  				{
  					Jaxer.DB.execute("INSERT INTO tasks (id, description, created) " +

  						"VALUES (?, ?, ?)",
  						[id, description, new Date()]);
  				}
  			}
  			// Because we want this function callable from the client, we set it's proxy
  			// value to true
  			saveTaskInDB.proxy = true;
   </textarea>               <p>
                      Use the capability of 
                      <tt>
                          DB.execute
                      </tt>. For example, instead of embedding input values into the SQL itself, which could expose your code to SQL injection attacks. Use question marks and pass in an array of values to be substituted respectively for the question marks. This also eliminates the need to escape the input values.
                  </p>
              </li>
              <li>
                  Set up your code to call 
                  <tt>
                      saveTask
                  </tt>
                  within 
                  <tt>
                      addTask
                  </tt>
                  from the client whenever a task is added. Also call this when the task description changes by adding it to the 
                  <tt>
                      onchange
                  </tt>
                  handler on the 
                  <tt>
                      &lt;input&gt;
                  </tt>
                  box of each task. Recall that these too are created by 
                  <tt>
                      addTask
                  </tt>, which now becomes:
  <textarea name="code" class="javascript">		<script type="text/javascript" runat="both">
  			function addTaskToUI(description, id)
  			{
  				var newId = id || Math.ceil(1000000000 * Math.random());
  				var div = document.createElement("div");
  				div.id = "task_" + newId;
  				div.className = "task";

  				var checkbox = document.createElement("input");
  				checkbox.setAttribute("type", "checkbox");
  				checkbox.setAttribute("title", "done");
  				checkbox.setAttribute("id", "checkbox_" + newId);
  				Jaxer.setEvent(checkbox, "onclick", "completeTask(" + newId + ")");
  				div.appendChild(checkbox);

  				var input = document.createElement("input");
  				input.setAttribute("type", "text");
  				input.setAttribute("size", "60");
  				input.setAttribute("title", "description");
  				input.setAttribute("id", "input_" + newId);
  				input.value = description;
  				Jaxer.setEvent(input, "onchange", "saveTaskInDB(" + newId + ", this.value)");
  				div.appendChild(input);

  				$("tasks").insertBefore(div, $("tasks").firstChild);

  				if (!Jaxer.isOnServer)
  				{
  					saveTaskInDB(newId, description);
  				}
  			}
  		</script>
  </textarea>            </li>
              <li>
                  To use 
                  <tt>
                      addTask
                  </tt>
                  on the server, you’ll need the 
                  <tt>
                      $(id)
                  </tt>
                  helper function  on the server, so add 
                  <tt>
                      $.runat="both";
                  </tt>
                  to your code.
              </li>
              <li>
                  Finally, when a task is checked off as done, delete it from the client and server. Change 
                  <tt>
                      completeTask
                  </tt>
                  to call a new server-side, client-proxied 
                  <tt>
                      deleteSavedTask
                  </tt>
                  function:
  <textarea name="code" class="html">			/*
  			 * Delete a task from the database
  			 */
  			function deleteSavedTask(id)
  			{
  				Jaxer.DB.execute("DELETE FROM tasks WHERE id = ?", [id]);
  			}
  			// Because we want this function callable from the client, we set it's proxy
  			// value to true
  			deleteSavedTask.proxy = true;

  			/*
  			 * This client function sets a task as completed and calls the server-side function
  			 * 'deleteSavedTask' to remove it from the database
  			 */
  			function completeTask(taskId)
  			{
  				var div = $("task_" + taskId);
  				div.parentNode.removeChild(div);
  				deleteSavedTask(taskId);
  			}
  </textarea>           </li>
              <p>
              </p>
          </ol>
          <p>
              This final step completes your application. You now have a simple Ajax tasks manager built entirely in one web page using only standard, web-native paradigms: HTML, JavaScript, and CSS with a bit of SQL on the server and some new JavaScript server-side functionality. The server modifies the HTML DOM based on some JavaScript code and the database, adds a few proxy functions and sends it to the client. The client allows the user to modify it based on new information using the same code, and seamlessly calls the server back to persist the changes to the database.
          </p>

          <a name="Complete_Code"></a>
          <h2>Complete Code</h2>
          <p>
              This page contains the entire code sample for the simple tasks application.
          </p>
  <textarea name="code" class="html">
  	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
  <html>
  	<head>
  		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
  		<title>Jaxer Tasks Sample Application</title>
  		<link rel='stylesheet' type='text/css' href='css/index.css'>
  		<style type="text/css">
  			.tasks { 
  				background-color: #f0f0ff; 
  				padding: 8px;
  			}

  			.new-task {
  				padding: 4px 0 4px 0; 
  				border-bottom: 3px solid #B5B5DF;
  			}

  			.task { 
  				padding: 4px; 
  			}
  		</style>

  		<!-- This script block will be available on both client and server since the 
  			runat attribute is set to 'both'. -->
  		<script type="text/javascript" runat="both">
  			/*
  			 * Easy access to a named element in the DOM
  			 */
  			function $(id) 
  			{ 
  				return document.getElementById(id); 
  			}

  			/*
  			 * 
  			 */
  			function addTaskToUI(description, id)
  			{
  				var newId = id || Math.ceil(1000000000 * Math.random());
  				var div = document.createElement("div");
  				div.id = "task_" + newId;
  				div.className = "task";

  				var checkbox = document.createElement("input");
  				checkbox.setAttribute("type", "checkbox");
  				checkbox.setAttribute("title", "done");
  				checkbox.setAttribute("id", "checkbox_" + newId);
  				Jaxer.setEvent(checkbox, "onclick", "completeTask(" + newId + ")");
  				div.appendChild(checkbox);

  				var input = document.createElement("input");
  				input.setAttribute("type", "text");
  				input.setAttribute("size", "60");
  				input.setAttribute("title", "description");
  				input.setAttribute("id", "input_" + newId);
  				input.value = description;
  				Jaxer.setEvent(input, "onchange", "saveTaskInDB(" + newId + ", this.value)");
  				div.appendChild(input);

  				$("tasks").insertBefore(div, $("tasks").firstChild);

  				if (!Jaxer.isOnServer)
  				{
  					saveTaskInDB(newId, description);
  				}
  			}
  		</script>

  		<!-- This script block will execute only on the server because of the
  			runat="server" attributes. -->
  		<script type="text/javascript" runat="server">

  			/*
  			 * The SQL to create the database table we'll use to store the tasks
  			 */
  			var sql = "CREATE TABLE IF NOT EXISTS tasks " +
  				"( id INTEGER NOT NULL" +
  				", description VARCHAR(255)" +
  				", created DATETIME NOT NULL" +
  				")";

  			// Execute the sql statement against the default Jaxer database
  			Jaxer.DB.execute(sql);

  			/*
  			 * Set the 'onserverload' property to call our function once the page has been fully
  			 * loaded server-side. We could have also set this attribute on the <body> tag of our
  			 * page and had it call a function by name.
  			 */
  			window.onserverload = function()
  			{
  				var resultSet = Jaxer.DB.execute("SELECT * FROM tasks ORDER BY created");
  				for (var i=0; i<resultSet.rows.length; i++)
  				{
  					var task = resultSet.rows[i];
  					addTaskToUI(task.description, task.id);
  				}
  			}

  			/*
  			 * Save a task directly into the database
  			 */
  			function saveTaskInDB(id, description)
  			{
  				var resultSet = Jaxer.DB.execute("SELECT * FROM tasks WHERE id = ?", [id]);
  				if (resultSet.rows.length > 0) // task already exists
  				{
  					Jaxer.DB.execute("UPDATE tasks SET description = ? WHERE id = ?",
  						[description, id]);
  				}
  				else // insert new task
  				{
  					Jaxer.DB.execute("INSERT INTO tasks (id, description, created) " +
  						"VALUES (?, ?, ?)",
  						[id, description, new Date()]);
  				}
  			}
  			// Because we want this function callable from the client, we set it's proxy
  			// value to true
  			saveTaskInDB.proxy = true;

  			/*
  			 * Delete a task from the database
  			 */
  			function deleteSavedTask(id)
  			{
  				Jaxer.DB.execute("DELETE FROM tasks WHERE id = ?", [id]);
  			}
  			// Because we want this function callable from the client, we set it's proxy
  			// value to true
  			deleteSavedTask.proxy = true;
  		</script>

  		<!-- This script block is a standard script block and runs on the browser only -->
  		<script type="text/javascript">

  			/*
  			 * This client function sets a task as completed and calls the server-side function
  			 * 'deleteSavedTask' to remove it from the database
  			 */
  			function completeTask(taskId)
  			{
  				var div = $("task_" + taskId);
  				div.parentNode.removeChild(div);
  				deleteSavedTask(taskId);
  			}

  			/*
  			 * Create a new task and add it to the user interface
  			 */
  			function newTask()
  			{
  				var description = $('txt_new').value;
  				if (description != '')
  				{
  					addTaskToUI(description);
  					$('txt_new').value = '';
  				}
  			}

  			/*
  			 * Create a new task if the enter key was hit
  			 */
  			function newKeyDown(evt)
  			{
  				if (evt.keyCode == 13)
  				{
  					newTask();
  					return false;
  				}
  			}

  		</script>

      </head>

  	<body>		
  		<script type="text/javascript" src="lib/wz_tooltip.js"></script>

  		<div id='sampleDescription'>
  			A simple tasks application where you can add, modify, and check-off (delete) to-do's.
  		</div>
  		<div id='sampleSource'>
  		<li><a href="/aptana/tools/sourceViewer/index.html?filename=../../samples/tasks/index.html" target="_blank">Chat Source Code</a></li>
  		</div>

  		<div id='sampleHeader'>
  			<div class='sampleTitle'>
  				<img src='images/date_edit.png'/> Tasks To Do
  			</div>
  			<div id='rightFloat'>
  				<img src ='images/information.png' class='sampleDescription' onmouseover="TagToTip('sampleDescription', CLICKCLOSE, true, STICKY, true, WIDTH, 300, TITLE, 'Sample Info')"/>
  				<span id='sourceButton'><img src ='images/html.png' 	   id='sampleSourceLink'  onmouseover="TagToTip('sampleSource', STICKY, true, CLOSEBTN, true,  TITLE, 'View Source Code')"/></span>
  			</div>
  		</div>

  		<div id='applicationContent'>
  		<div class="new-task">
  			New:
  			<input type="text" id="txt_new" size="60" onkeydown="newKeyDown(event)">
  			<input type="button" value="add" onclick="newTask()">
  		</div>
  		<div id="tasks" class="tasks">
  		</div>
  		</div>

  		<div id='sampleFooter'>
  		<BR><i>Any changes should be automatically saved to your database!</i>			
  		</div>

  		<script runat='server'>
  				if (Jaxer.System.executableFolder.match('com.aptana.ide.framework.jaxer')) {
  					document.getElementById('sampleSource').innerHTML="";
  					document.getElementById('sourceButton').innerHTML="";
  				}
  		</script> 
      </body>
  </html>

  </textarea>
<?php include('../includes/footer.php'); ?>
