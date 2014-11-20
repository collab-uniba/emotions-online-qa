package csv;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Iterator;
import java.util.StringTokenizer;

import stemming.Snowball;
import cc.mallet.types.Instance;

public class CSVIterator  implements Iterator<Instance>{

	Iterator<CSVRecord> it_records;
	boolean first = true;
	boolean with_stemming = false;
	
	public CSVIterator(String inputFile, boolean with_stemming) throws IOException {
		// TODO Auto-generated constructor stub
		this.with_stemming = with_stemming;
		Reader in = new InputStreamReader(new FileInputStream(new File(inputFile)), "UTF-8");
		Iterable<CSVRecord> records = CSVFormat.newFormat(';').withRecordSeparator("\r\n").withQuoteChar('"').parse(in);
		it_records = records.iterator();
		//in.close();
	}
	
	public static String cleanTags(String tags){
		String tags_cleaned;
		if(!tags.equals("None")){
			tags_cleaned = tags.replace(">", " ").replace("<", "");
		}else{
			tags_cleaned = tags;
		}
		return tags_cleaned;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean hasNext() {
		// TODO Auto-generated method stub
		return it_records.hasNext();
	}

	@Override
	public Instance next() {
		// TODO Auto-generated method stub
		String data = "";
		String stemmed_field = "";
		CSVRecord record = it_records.next();
			
		if(first){
			record = it_records.next();
			first = false;
		}
		
		Iterator<String> it = record.iterator();
		int count = 0;
		//boolean print = false;
		while(it.hasNext()){
			String current_field = (String)it.next();
			data = "";
			//if(count == 0 & current_field.equals("73"))
			//	print = true;
			if(count == 1 /*| count == 2*/){ // Corpus
				try {
					if(this.with_stemming)
						data = Snowball.extract_stem_corpus(current_field); // Extract stems
					else
						data = current_field;
					//data = current_field;
					//if(print)
					//	System.out.println(data);
				} catch (ClassNotFoundException | InstantiationException
						| IllegalAccessException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				//data = data + stemmed_field + " "; // Use stemmed field (title or body)
			}//else if(count == 3)
			//	data = data + cleanTags(current_field) + " ";
				
			count++;
		}
		Instance carrier = new Instance (data, null, null, null);
		//System.err.println("Instance");
		//System.out.println(carrier.getData());
		
		return carrier;
	}

	@Override
	public void remove() {
		// TODO Auto-generated method stub
		
	}

}
