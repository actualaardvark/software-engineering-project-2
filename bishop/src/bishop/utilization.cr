# There's a memory leak either here or in the svelte component that uses this.
require "json"
require "hardware"

module Bishop
  # Contains live updating resource utilization data.
  class Utilization
    # `Hardware::CPU` and `Hardware::Memory` work differently.
    # The CPU object refreshes each time the methods are called.
    # The memory object captures values when created and does not update them.
    include JSON::Serializable
    private CPU = Hardware::CPU.new

    # Converts Time values to nanoseconds since the Unix epoch.
    # ```
    # require "json"
    #
    # class Example
    #   include JSON::Serializable
    #
    #   @[JSON::Field(converter: Bishop::Utilization::UnixNanosecondsConverter)]
    #   property time : Time
    #
    #   def initialize(time)
    #     @time = time
    #   end
    # end
    #
    # example = Example.new Time.utc(1999, 1, 1, 0, 0, 0)
    #
    # example.to_json # => {"time" : 915148800000000000}
    # ```
    class UnixNanosecondsConverter
      def self.to_json(value : Time, builder : JSON::Builder) : JSON::Builder
        builder.number(value.to_unix_ns) # Returns nil so we have to return it on the next line instead.
        builder
      end
    end

    property cpu_usage : Int32
    property memory_usage : Int32
    property memory_total : Int32

    @[JSON::Field(converter: Bishop::Utilization::UnixNanosecondsConverter)]
    property last_update : Time

    def initialize
      @cpu_usage = 0
      @memory_usage = 0
      @memory_total = Hardware::Memory.new.total
      @last_update = Time.utc

      # Spawns a thread with a loop.
      # Every half-second the values are updated and then the update is timestamped.
      spawn do
        loop do
          sleep 500.milliseconds
          @memory_usage = Hardware::Memory.new.percent.to_i
          @cpu_usage = CPU.usage!.to_i
          @last_update = Time.utc
        end
      end
    end
  end
end
