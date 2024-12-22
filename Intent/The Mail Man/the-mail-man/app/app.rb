require 'sinatra'
require 'sinatra/reloader' if development?
require 'mysql2'
require 'securerandom'
require 'mail'
require 'bcrypt'
require 'puma'

enable :sessions

DB = Mysql2::Client.new(
  host: 'db',
  username: 'root',
  password: 'password',
  database: 'ctf_challenge'
)

admin_email = 'admin@localhost'
admin_password = BCrypt::Password.create(SecureRandom.hex(16)) 

DB.query("CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  admin BOOLEAN DEFAULT FALSE
)")
DB.query("INSERT IGNORE INTO users (email, password, admin) VALUES ('#{admin_email}', '#{admin_password}', true)")

 
get '/' do
  if session[:email]
    @user = session[:email]
  end
  erb :home
end

get '/register' do
  erb :register
end

post '/register' do
  raw_email = params[:email]
  password = params[:password]

  existing_user = DB.prepare("SELECT * FROM users WHERE email = ?").execute(raw_email).first

  if existing_user
    @error = 'Email already registered.'
    return erb :register
  end

  if raw_email.include?('admin')
    @error = 'Registration with "admin" in the username is not allowed.'
    return erb :register
  end

  hashed_password = BCrypt::Password.create(password)

  begin
    DB.prepare("INSERT INTO users (email, password) VALUES (?, ?)").execute(raw_email, hashed_password)
    @success = 'Registration successful. You can now login.'
    erb :login
  rescue Mysql2::Error => e
    @error = "An error occurred during registration"
    erb :register
  end
end

get '/login' do
  erb :login
end

post '/login' do
  raw_email = params[:email]
  password = params[:password]
  if raw_email && !raw_email.empty?
    result = DB.prepare("SELECT * FROM users WHERE email = ?").execute(raw_email).first
  else
    @error = "Invalid email input"
  end  

  if result && BCrypt::Password.new(result['password']) == password
    email = Mail::Address.new(raw_email).address
    session[:email] = email
    redirect '/'
  else
    @error = 'Invalid email or password.'
    erb :login
  end
end

get '/admin' do
  if session[:email] == 'admin@localhost'
    @flag = ENV['FLAG'] || 'No Flag Set'
    erb :admin
  else
    status 403
    'Forbidden: Admins only.'
    redirect '/login'
  end
end


get '/logout' do
  session.clear
  redirect '/'
end
