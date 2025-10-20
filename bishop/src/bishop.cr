require "kemal"
require "db"
require "sqlite3"
require "uri"
require "log"
require "digest/sha256"
require "json"
require "./bishop/utilization"

module Bishop
  Log               = ::Log.for("bishop")
  VERSION           = "0.1.0"
  DB_PATH           = Path.new "./bishop.db"
  DB_URI            = URI.new(scheme: "sqlite3", host: DB_PATH.to_s)
  TABLE_NAME        = "jobs"
  CUSTOM_DB         = DBHandler.new(DB_URI)
  MAX_NOTEBOOK_SIZE = 5 * 1024 * 1024

  @@admin_username : String? = begin
    ENV["CHESSBOARD_ADMIN_USERNAME"]
  rescue KeyError
    nil
  end

  @@admin_password : String? = begin
    ENV["CHESSBOARD_ADMIN_PASSWORD"]
  rescue KeyError
    nil
  end

  @@admin_features_disabled : Bool = @@admin_password.nil? || @@admin_username.nil?

  # TODO: Actually make this do something.
  if @@admin_features_disabled
    Log.info { "Admin environment key(s) unset. Admin features disabled." }
  else
    Log.info { "Admin environment keys set. Admin features enabled." }
  end

  CUSTOM_DB.create_base_table
  CUSTOM_DB.create_job(Path.new("./tmp"))

  private UTILIZATION = Bishop::Utilization.new

  enum APIResult
    Success
    Error
  end

  class APIResponse
    include JSON::Serializable

    property result : APIResult
    property error_message : String?

    def initialize(@result : APIResult, @error_message : String? = nil, **args)
    end
  end

  # Send resource utilization each second.
  ws "/api/v1/socket/monitor/global" do |socket|
    loop do
      sleep 1.second
      socket.send(UTILIZATION.to_json)
    end
  end

  # Upload files route.
  post "/api/v1/jobs/create" do |env|
    uploaded_file = env.params.files["notebook"]

    print(uploaded_file)

    # Check file size.

    uploaded_file_size = uploaded_file.size

    if uploaded_file_size.nil?
      halt env, status_code: 400, response: APIResponse.new(
        result: APIResult::Error,
        error_message: "File is empty"
      ).to_json
    elsif uploaded_file_size > MAX_NOTEBOOK_SIZE
      halt env, status_code: 400, response: APIResponse.new(
        result: APIResult::Error,
        error_message: "File size exceeded max notebook size"
      ).to_json
    end

    # Check file extension.
    allowed_extensions = [".ipynb"]
    file_extension = File.extname(uploaded_file.filename || "").downcase

    unless allowed_extensions.includes?(file_extension)
      halt env, status_code: 400, response: "Invalid file extension"
    end

    APIResponse.new(result: APIResult::Success).to_json
  end

  Kemal.run

  class Job
    include DB::Serializable
    include JSON::Serializable

    property hash : String
    property creation_date : Time
    property? complete : Bool
    property completion_date : Time
    property? useless : Bool
  end

  struct DBHandler
    Log = Bishop::Log.for("dbhandler")

    def initialize(@db_uri : URI)
    end

    def create_job(job_notebook_path : Path)
      DB.open @db_uri do |database|
        digest = Digest::SHA256.new
        digest.update(File.read job_notebook_path)
        id : String = digest.final.hexstring

        database.exec "insert into jobs values (?, ?, ?, ?, ?)", id, Time.utc.to_s, false, "", false
      end
    end

    private def jobs_table_exists?
      DB.open @db_uri do |database|
        exists = File.exists?(DB_PATH)
        has_jobs_table = begin
          database.query_one "SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'", as: {String}
          true
        rescue DB::NoResultsError
          false
        end
        exists && has_jobs_table
      end
    end

    def create_base_table
      DB.open @db_uri do |database|
        if jobs_table_exists?()
          Log.info { "Table '#{TABLE_NAME}' already exists. '#{TABLE_NAME}' will not be recreated." }
        else
          Log.info { "Table '#{TABLE_NAME}' does not exist. '#{TABLE_NAME}' will be created." }
          database.exec "CREATE table jobs (hash text, creation_date text, complete boolean, completion_date text, useless boolean)"
        end
      end
    end
  end
end
