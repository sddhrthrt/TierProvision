package smartpath;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

//import okhttp3.FormBody
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
/**
 * @author abhishek
 */


class JobCreateResponse {
	private String EvalCreateIndex;
	private String EvalID;
	private int Index;
	public int JobModifyIndex;
	private boolean KnownLeader;
	private int LastContact;
	private String Warnings;
	// Getters ans setters not required for this mock, GSON sets the fields using reflection.
}

public class JobHttpServer {
	
		private static String nomadurl = "http://127.0.0.1:4646";
		private static int job_modify_indx;
		
        public static void main(String[] args) throws Exception {
                HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
                server.createContext("/submitjob", new JobHandler());
                server.createContext("/modifyjob", new JobModHandler());
                server.setExecutor(null); // creates a default executor
                server.start();
        }

        static class JobHandler implements HttpHandler {
                public void handle(HttpExchange t) throws IOException {
                        String job =
                        "{\r\n"+
                        "    \"Job\": {\r\n"+
                        "        \"ID\": \"docs\",\r\n"+
                        "        \"Name\": \"docs\",\r\n"+
                        "        \"Datacenters\": [\r\n"+
                        "            \"dc1\"\r\n"+
                        "        ],\r\n"+
                        "        \"TaskGroups\": [{\r\n"+
                        "            \"Name\": \"example\",\r\n"+
                        "            \"Count\": 1,\r\n"+
                        "            \"Tasks\": [{\r\n"+
                        "               \"Name\": \"server\",\r\n"+
                        "               \"Driver\": \"docker\",\r\n"+
	                        "                \"Config\": {\r\n"+
                        "                    \"image\": \"hashicorp/http-echo\",\r\n"+
                        "                    \"args\": [\r\n"+
                        "                        \"-listen\",\r\n"+
                        "                        \":5678\",\r\n"+
                        "                        \"-text\",\r\n"+
                        "                        \"Hello World\"\r\n"+
                        "                    ]\r\n"+
                        "                },\r\n"+
                        "                \"Resources\": {\r\n"+
                        "				 	 \"CPU\": 1000,\r\n"+
                        "					 \"MemoryMB\": 512,\r\n" +
                        "                    \"Networks\": [{\r\n"+
                        "                        \"MBits\": 10,\r\n"+
                        "                        \"StaticPorts\": [{\r\n"+
                        "                            \"Label\": \"http\",\r\n"+
                        "                            \"Value\": \"5678\"\r\n"+
                        "                        }]\r\n"+
                        "                    }]\r\n"+
                        "                }\r\n"+
                        "            }]\r\n"+
                        "        }],\r\n"+
                        "        \"Update\": {\r\n"+
                        "            \"MaxParallel\": 1\r\n"+
                        "        }\r\n"+
                        "    }\r\n"+
                        "}";
                        System.out.println(job);

                        RequestBody body = RequestBody.create( MediaType.parse("application/json"),job);
                        Request request = new Request.Builder().url(nomadurl+"/v1/jobs").post(body).build();

                        System.out.println("After Request");
                        Response response;
                        String response_str="Couldnt submit job";
                        try {
                        	    System.out.println("In Try");
                                response = new OkHttpClient().newCall(request).execute();
                                response_str=response.body().string();
                                response.close();
                        } catch (IOException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                        }

                        System.out.println(response_str);
                        Gson gson_builder = new GsonBuilder().create();
                        JobCreateResponse job_create_response = 
                        		gson_builder.fromJson(response_str, JobCreateResponse.class);
                        job_modify_indx = job_create_response.JobModifyIndex;
                        t.sendResponseHeaders(200, response_str.length());
                        OutputStream os = t.getResponseBody();
                        os.write(response_str.getBytes());
                        os.close();
                }
        }
        
        static class JobModHandler implements HttpHandler {
            public void handle(HttpExchange t) throws IOException {
                    String job =
                    "{\r\n"+
                    "    \"Job\": {\r\n"+
                    "        \"ID\": \"docs\",\r\n"+
                    "        \"Name\": \"docs\",\r\n"+
                    "        \"Datacenters\": [\r\n"+
                    "            \"dc1\"\r\n"+
                    "        ],\r\n"+
                    "        \"TaskGroups\": [{\r\n"+
                    "            \"Name\": \"example\",\r\n"+
                    "            \"Count\": 1,\r\n"+
                    "            \"Tasks\": [{\r\n"+
                    "                \"Name\": \"server\",\r\n"+
                    "               \"Driver\": \"docker\",\r\n"+
                        "                \"Config\": {\r\n"+
                    "                    \"image\": \"hashicorp/http-echo\",\r\n"+
                    "                    \"args\": [\r\n"+
                    "                        \"-listen\",\r\n"+
                    "                        \":5678\",\r\n"+
                    "                        \"-text\",\r\n"+
                    "                        \"Hello World\"\r\n"+
                    "                    ]\r\n"+
                    "                },\r\n"+
                    "                \"Resources\": {\r\n"+
                    "				 	 \"CPU\": 500,\r\n"+
                    "					 \"MemoryMB\": 215,\r\n" +
                    "                    \"Networks\": [{\r\n"+
                    "                        \"MBits\": 10,\r\n"+
                    "                        \"StaticPorts\": [{\r\n"+
                    "                            \"Label\": \"http\",\r\n"+
                    "                            \"Value\": \"5678\"\r\n"+
                    "                        }]\r\n"+
                    "                    }]\r\n"+
                    "                }\r\n"+
                    "            }]\r\n"+
                    "        }],\r\n"+
                    "        \"Update\": {\r\n"+
                    "            \"MaxParallel\": 1\r\n"+
                    "        }\r\n"+
                    "    },\r\n"+
                    "    \"EnforcementIndex\": true,\r\n"+
                    "    \"JobModifyIndex\": " + job_modify_indx + "\r\n" +
                    "}";
                    System.out.println(job);

                    RequestBody body = RequestBody.create( MediaType.parse("application/json"),job);
                    Request request = new Request.Builder().url(nomadurl+"/v1/jobs").post(body).build();

                    System.out.println("After Request");
                    Response response;
                    String response_str="Couldnt submit job";
                    try {
                    	    System.out.println("In Try");
                            response = new OkHttpClient().newCall(request).execute();
                            response_str=response.body().string();
                            response.close();
                    } catch (IOException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                    }

                    System.out.println(response_str);
                    t.sendResponseHeaders(200, response_str.length());
                    OutputStream os = t.getResponseBody();
                    os.write(response_str.getBytes());
                    os.close();
            }
    }
}