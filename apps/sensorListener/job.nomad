job "sensorListener" {
  region = "global"
  datacenters = ["dc1"]
  type = "service"
  group "server" {
    count = 1
    task "API" {
      driver = "docker"
      config {
        image = "sddhrthrt/sensorlistener:0.1.1"
      }
      service {
        port = "http"
        check {
          type     = "http"
          path     = "/ping"
          interval = "10s"
          timeout  = "2s"
        }
      }
      env {
      }
      resources {
        cpu    = 500 # MHz
        memory = 128 # MB
        network {
          mbits = 100
          port "http" {}
          port "https" {
            static = 443
          }
        }
      }
    }
  }
}
