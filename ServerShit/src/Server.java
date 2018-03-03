import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Properties;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.LongSerializer;
import org.apache.kafka.common.serialization.StringSerializer;


public class Server {
	private static ServerSocket serverSocket;
	Thread serverThread = null;
	static Socket socket = null;
	public static final int SERVERPORT = 8000;

			
	public static void main(String[] args){
		try {
			serverSocket = new ServerSocket(SERVERPORT);
		} catch (IOException e) {
			e.printStackTrace();
		}
		while(true) {
			try {
				socket = serverSocket.accept();
				FuckThread shit = new FuckThread();
				shit.clientSocket = socket;
				Thread t=new Thread(shit);
				t.start();

			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	
	}
	
	
}
class FuckThread implements Runnable{
    Socket clientSocket;
    private BufferedReader input;
    private final static String TOPIC = "test";
    private final static String BOOTSTRAP_SERVERS = "192.168.0.40:9092";
   
	
    
    private static Producer<Long, String> createProducer() {
	        Properties props = new Properties();
	        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
	                                            BOOTSTRAP_SERVERS);
	        props.put(ProducerConfig.CLIENT_ID_CONFIG, "KafkaExampleProducer");
	        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
	                                        LongSerializer.class.getName());
	        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
	                                    StringSerializer.class.getName());
	        return new KafkaProducer<>(props);
	   }
	@Override
	public void run() {
		// TODO Auto-generated method stub.
		System.out.println("CLient Connected");
	     Producer<Long, String> producer = createProducer();
		  try {
			this.input = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
			String l = input.readLine();
			  while(l != null){
				  System.out.println(l);
				  KafkaProducerExample.runProducer(l, producer);
			      producer.flush();
				  l = input.readLine();
		    }
			 System.out.println("client terminated");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally{
	        producer.flush();
			producer.close();
		}
		 
	}
	
}

	
	
	

	
			
			
		
	
	