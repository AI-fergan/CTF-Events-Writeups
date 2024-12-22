require './app'
set :host_authorization, { permitted_hosts: ["the-mail-man.ctf.intentsummit.org", "localhost", "127.0.0.1"] }
run Sinatra::Application
