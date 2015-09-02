require "logger"

require "que/rake_tasks"

task :environment do
  require "sequel"
  db = Sequel.connect(ENV.fetch("DATABASE_URL"))

  require "que"
  Que.connection = db
  Que.logger = Logger.new(STDOUT)

  require_relative "lib/taxonomist"
end

desc "Run Pry"
task :pry do
  require_relative "lib/taxonomist"
  include Taxonomist

  require "dotenv"
  Dotenv.load(".test.envrc")

  api_key = ENV.fetch("TWITTER_API_KEY")
  api_secret = ENV.fetch("TWITTER_API_SECRET")
  access_token = ENV.fetch("TWITTER_ACCESS_TOKEN")
  access_token_secret = ENV.fetch("TWITTER_ACCESS_TOKEN_SECRET")

  twitter = Twitter::Authed.new(api_key: api_key,
                                api_secret: api_secret,
                                access_token: access_token,
                                access_token_secret: access_token_secret)

  user = Models::User[25]
  class QueJob < Sequel::Model; end

  require "pry"
  binding.pry
end

namespace :db do
  desc "Run migrations"
  task :migrate, [:version] => 'que:migrate' do |t, args|
    Sequel.extension :migration

    if args[:version]
      puts "Migrating to version #{args[:version]}"
      Sequel::Migrator.run(db, "db/migrations", target: args[:version].to_i)
    else
      puts "Migrating to latest"
      Sequel::Migrator.run(db, "db/migrations")
    end

    db.extension :schema_dumper
    File.write("db/schema.rb",
               db.dump_schema_migration(same_db: true).gsub(/^\s+$/, ''))
  end
end