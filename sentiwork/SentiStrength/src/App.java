import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.Writer;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Iterator;
import java.util.LinkedList;

import uk.ac.wlv.sentistrength.*;
import csv.*;

public class App {

	private static String input_file_dir = "input_file/";
	private static String output_file_dir = "output_file/";
	private static String download_file_dir = "download/";
	private static SentiStrength sentiStrength = null;
	private static Corpus corpus = null;
	
	private static String protocol = "http://";
	private static String host = "localhost";
	private static String port = ":80";
	private static String sep = "/";
	
	private static String db_req = "databases";
	private static String query_req = "queries";
	private static String process_req = "process";
	
	private static String answers_query = "SELECT%20Id%2C%20Body%2C%20CreationDate%20FROM%20Posts%20WHERE%20PostTypeId%20%3D%202%20AND%20creationDate%20BETWEEN%20%272014-01-01%27%20AND%20%272014-01-07%27";
	private static String posts_query = "SELECT%20Id%2C%20Tags%20FROM%20Posts";
	
	private static String stackoverflow_db = "stackoverflow.db";
	private static String italian_db = "italian.stackexchange.dump.db";
	
	
	public App(){
		initialize();
		initializeCorpus();
	}
	
	// Inizializza oggetto SentiStrength per la classificazione
	public static void initialize(){
		sentiStrength = new SentiStrength();
		String ssthInitialisation[] = {"sentidata", "lib/SentiStrength_Data/", "explain"};
		sentiStrength.initialise(ssthInitialisation);
	}
	
	public static void initializeCorpus(){
		corpus = sentiStrength.getCorpus();
	}
	
	/*
	 *  Analizza il file 'inputFile' (che deve essere in formato CSV) prendendo la colonna body_column
	 *  e scrive il risultato dell'analisi di SentiStrength nel file 'outputFile'
	 *  
	 *  	@param
	 *  		inputFile:		path del file di input in formato CSV
	 *  		outputFile:		path del file su cui scrivere i risultati
	 *  		body_column:	colonna che contiene il testo da analizzare
	 */			
	public void analizeCSV(String inputFile, String outputFile, int body_column) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(outputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		
		for (CSVRecord record : records) {
			
			// Campi
			String body = record.get(body_column-1);
			
			// Classificazione
			String score = sentiStrength.computeSentimentScores(body);
			String[] split_res = score.split(" ");
			String pos_score = split_res[0];
			String neg_score = split_res[1];
			
			// Stampa a video
			System.err.print("Body: ");
			System.out.println(body);
			System.err.print("Positive score: ");
			System.out.println(pos_score + "\n");
			System.err.print("Negative score: ");
			System.out.println(neg_score + "\n");
			
			printer_csv.print(pos_score);
			printer_csv.print(neg_score);
			printer_csv.print(body);
			printer_csv.println();
			
			// Scrive sul file
			//out.write(score + "\n\n\n###################################################\n\n\n");
		}
		//out.close();
		printer_csv.close();
	}
	
	public void listTagsAverage(String inputFile, int body_column) throws IOException{
		Reader in = new FileReader(inputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		LinkedList<String> tags = new LinkedList<String>();
		
		int no_tag_post = 0;
		int quest_no_tag = 0;
		int answ_no_tag = 0;
		int quest = 0;
		int answ = 0;
		int max_tag = 0;
		int num_records = 0;
		int num_tags = 0;
		int part_value = 0;
		float tags_p_quest = 0;
		float average = 0;
		boolean first = true;
		
		for (CSVRecord record : records) {
			if(first == false){
				num_records++;
				
				String post_type = record.get(2);
				String field_tags = record.get(body_column-1);
				String[] splitted_field = field_tags.split(">");
				int len = splitted_field.length;
				
				if(post_type.equals("1"))
					quest++;
				else if(post_type.equals("2"))
					answ++;
				
				if(max_tag < len)
					max_tag = len;
				
				if(!splitted_field[0].equals("None")){
					part_value = part_value + len;
					//System.out.println("Tags: " + len);
					
					for(int i=0; i < len; i++){
						String tag = splitted_field[i].replace("<", "");
						if(!tags.contains(tag)){
							tags.add(tag);
						}
							
					}
				}else{
					no_tag_post++;
					if(post_type.equals("1"))
						quest_no_tag++;
					else if(post_type.equals("2"))
						answ_no_tag++;
				}
			}
			else
				first = false;
		}
		
		average = (float)part_value/(float)num_records;
		tags_p_quest = (float)part_value/(float)quest;
		
		Writer out = new FileWriter("tags.txt");
		out.write("Tags identified:\n");
		Iterator<String> it = tags.iterator();
		while(it.hasNext()){
			num_tags++;
			out.write("\t"+it.next()+"\n");
		}
		
		System.out.println("Part: " + part_value);
		
		
		out.write("\nNumber of tags: " + num_tags + "\n" +
					"Number of posts: " + num_records + "\n" +
					"Number of questions: " + quest + "\n" +
					"Number of answers: " + answ + "\n" +
					"Number of posts with no tag: " + no_tag_post + "\n" +
					"Number of questions with no tag: " + quest_no_tag + "\n" +
					"Number of answers with no tag: " + answ_no_tag + "\n" +
					"Max tags received by a post: " + max_tag + "\n" +
					"Average of tags per posts: "+ average + "\n" +
					"Average of tags per questions: "+ tags_p_quest + "\n"/* +
					"Average of tags in answers: "+ average + "\n"*/);
		
		out.close();
	}
	
	/*
	 * Restituisce in input il file CSV contenente per ogni riga, riferita ad un post, i tag del post 
	 */
	public void cleanTagsCSV(String inputFile, String outputFile, int body_column) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(outputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		
		for (CSVRecord record : records) {
			String tags_field = record.get(body_column-1);
			String tags_cleaned = tags_field.replace(">", " ").replace("<", "");
			printer_csv.print(tags_cleaned);
			printer_csv.println();
		}
		printer_csv.close();
	}
	
	/*
	 *  Prende in input il file da analizzare che deve avere su ogni riga la frase da analizzare,
	 *  scrive in output il risultato dell'analisi
	 */
	public void analizeLines(String inputFile, String outputFile){
		corpus.classifyAllLinesInInputFile(inputFile, outputFile);
	}
	
	/*
	 * Prende in input il file da analizzare, che deve avere su ogni riga la frase da analizzare,
	 * e il numero della riga su cui si trova la frase da analizzare. Stampa il risultato a video
	 * 
	 */ 
	public void analizeOneLine(String inputFile, int line){
		corpus.setCorpus(inputFile);
		
		//corpus.calculateCorpusSentimentScores();
		System.out.println( /*"BaselinePositiveAccuracyProportion: " + corpus.getBaselinePositiveAccuracyProportion() + "\n" +
							"BaselineNegativeAccuracyProportion: " + corpus.getBaselineNegativeAccuracyProportion() + "\n\n" +
							
							"ClassificationPositiveAccuracyProportion: " + corpus.getClassificationPositiveAccuracyProportion() + "\n" +
							"ClassificationNegativeAccuracyProportion: " + corpus.getClassificationNegativeAccuracyProportion() + "\n\n" +
							
							"ClassificationPositiveMeanDifference: " + corpus.getClassificationPositiveMeanDifference() + "\n" +
							"ClassificationNegativeMeanDifference: " + corpus.getClassificationNegativeMeanDifference() + "\n\n" +
							
							"ClassificationPositiveNumberCorrect: " + corpus.getClassificationPositiveNumberCorrect() + "\n" +
							"ClassificationNegativeNumberCorrect: " + corpus.getClassificationNegativeNumberCorrect() + "\n\n" +
									
							"ClassificationPositiveTotalDifference: " + corpus.getClassificationPositiveTotalDifference() + "\n" +
							"ClassificationNegativeTotalDifference: " + corpus.getClassificationNegativeTotalDifference() + "\n\n" +
									
							"ClassificationPosCorrelationWholeCorpus: " + corpus.getClassificationPosCorrelationWholeCorpus() + "\n" +
							"ClassificationNegCorrelationWholeCorpus: " + corpus.getClassificationNegCorrelationWholeCorpus() + "\n\n" +
									
							"CorpusMemberPositiveSentimentScore(1): " + corpus.getCorpusMemberPositiveSentimentScore(1) + "\n" +
							"CorpusMemberNegativeSentimentScore(1): " + corpus.getCorpusMemberNegativeSentimentScore(1) + "\n\n" +*/
									
							"CorpusMemberPositiveSentimentScore("+line+"): " + corpus.getCorpusMemberPositiveSentimentScore(line) + "\n" +
							"CorpusMemberNegativeSentimentScore("+line+"): " + corpus.getCorpusMemberNegativeSentimentScore(line));
		
	}
	
	public static void downloadCSV(String db, String query, String path_to_save){
		try {
			  URL url = new URL(protocol+host+port+sep+db_req+sep+db+sep+query_req+sep+query+sep+process_req+sep);
			  HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			  System.out.println("Timeout: " + connection.getReadTimeout());
			  BufferedReader read = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			  String line = read.readLine();
			  String res = "";
			  while(line!=null) {
			    res += line + "\n";
			    line = read.readLine();
			  }
			  Writer out = new FileWriter(path_to_save);
			  out.write(res);
			  out.close();
			  //System.out.println(res);
		} catch(MalformedURLException ex) {
		      ex.printStackTrace();
		} catch(IOException ioex) {
		      ioex.printStackTrace();
		}
	}
	
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		//App.downloadCSV(App.stackoverflow_db, App.posts_query, /*App.download_file_dir + */"downloaded.csv");
		
		App app = new App();
		app.cleanTagsCSV("it_tags.csv", "it_tags_cleaned.csv", 2);
		//app.listTagsAverage(/*App.download_file_dir + */"so_tags.csv", 2);
		//app.analizeCSV(input_file_dir + "downloaded.csv", output_file_dir + "result-set_out.csv", 2);
		//app.analizeLines(input_file_dir + "input.txt", output_file_dir + "output.txt");
		//app.analizeOneLine(input_file_dir + "input.txt", 1);
		
	}

}
