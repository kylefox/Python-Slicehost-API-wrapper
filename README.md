A small utility for working with the [Slicehost API](http://articles.slicehost.com/2008/5/13/slicemanager-api-documentation).

The `slicehost` module features common actions like creating default A and NS records, as well as MX records for Google Apps.  `slicehost_client.py` provides a command-line interface for convenience.

Requires the spectacular [pyactiveresource](http://code.google.com/p/pyactiveresource/), which does the majority of the work here :)

**Questions / Patches / Bugs?** [Send me a message](http://github.com/inbox/new/kylefox) via github.

Module Usage
------------

Create an instance of the wrapper by passing your API Key:

    from slicehost import *
    host = Slicehost("MY_API_KEY")
    
Once you've done that you can invoke standard [ActiveResource methods](http://api.rubyonrails.org/files/vendor/rails/activeresource/README.html) on the `Slice`, `Zone` and `Record` resources:
    
    my_slices = host.Slice.find()
    zone = host.Zone.find_first(origin="example.com")
    
The main goal of `python-slicehost` is to add Slicehost-specific helpers to the functionality that pyactiveresource already includes, like adding **default A-Records**

    # Creates A-Records pointing this zone & subdomains to a slice.
    a_record = zone.create_A_record(my_slices[0])
  
creating *NS-records pointing to slicehost*

    zone.setup_slicehost_ns()
    
and setting up **MX-Records for [Google Apps](http://www.google.com/a/)**

    zone.setup_google_apps()
    
Check the source -- it's pretty simple.  `slicehost_client.py` also includes example usage.

Command-line Client
------------------

The command-line client provides a quick and interactive interface for creating A-Records, NS-Records and Google MX-Records.  Pass in your API key (as plain-text or a filename) and follow the prompts :)

Passing your API key directly:

    [prompt]: python slicehost_client.py myawesomeapikey
    
Passing the filename that contains your API key:

    [prompt]: python slicehost_client.py apikey.txt
