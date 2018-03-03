import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.LongSerializer;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class KafkaProducerExample {
	   private final static String TOPIC = "test";
	   private final static String BOOTSTRAP_SERVERS = "192.168.0.40:9092";
	   
	   
	   static void runProducer(String message, Producer producer) throws InterruptedException {
		    

		    try {
		    	final ProducerRecord<Long, String> record =	 new ProducerRecord<>(TOPIC, message);
		    	producer.send(record);
		    	
		        /*for (long index = time; index < time + sendMessageCount; index++) {
		            final ProducerRecord<Long, String> record =
		                    new ProducerRecord<>(TOPIC, index, "Hello Mom " + index);
		            producer.send(record, (metadata, exception) -> {
		                long elapsedTime = System.currentTimeMillis() - time;
		                if (metadata != null) {
		                    System.out.printf("sent record(key=%s value=%s) " +
		                                    "meta(partition=%d, offset=%d) time=%d\n",
		                            record.key(), record.value(), metadata.partition(),
		                            metadata.offset(), elapsedTime);
		                } else {
		                    exception.printStackTrace();
		                }
		                countDownLatch.countDown();
		            });
		        }
		        */
		    }finally {
		    	
		    }
		}



}
