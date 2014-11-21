import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Formatter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Locale;
import java.util.Properties;
import java.util.StringTokenizer;
import java.util.regex.Pattern;

import edu.stanford.nlp.*;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.sentiment.SentimentPipeline;
import edu.stanford.nlp.util.CoreMap;
import uk.ac.wlv.sentistrength.*;
import csv.*;
import cc.mallet.util.*;
import cc.mallet.types.*;
import cc.mallet.pipe.*;
import cc.mallet.pipe.iterator.*;
import cc.mallet.topics.*;


public class App {

	private static StanfordCoreNLP tokenizer;
	private static StanfordCoreNLP pipeline;
	
	private static HashMap<String,String> LIWC;
	
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

	
	public App() throws IOException{
		initializeSentiStrength();
		initializeCorpus();
		loadLIWC();
	}
	
	// Inizializza oggetto SentiStrength per la classificazione
	public static void initializeSentiStrength(){
		sentiStrength = new SentiStrength();
		String ssthInitialisation[] = {"sentidata", "lib/SentiStrength_Data/", "explain"};
		sentiStrength.initialise(ssthInitialisation);
	}
	
	public static void initializeCorpus(){
		corpus = sentiStrength.getCorpus();
	}
	
	public static void initializeNLP(){
		Properties pipelineProps = new Properties();
	    //pipelineProps.setProperty("ssplit.eolonly", "true");
	    pipelineProps.setProperty("annotators", "tokenize,pos,cleanxml,parse,sentiment");
	    pipelineProps.setProperty("enforceRequirements", "false");
	    
	    Properties tokenizerProps = new Properties();
	    tokenizerProps.setProperty("annotators", /*"tokenize, ssplit"*/"tokenize,cleanxml,ssplit,pos,lemma,parse,sentiment");
	    
	    tokenizer = new StanfordCoreNLP(tokenizerProps);
	    pipeline = new StanfordCoreNLP(pipelineProps);
	    
	}
	
	public static void loadLIWC() throws IOException{
		LIWC = new <String,String>HashMap();
		Reader in = new FileReader("LIWC[1].all.txt");
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		
		for (CSVRecord record : records) {
			String key = record.get(0);
			String aff_class = record.get(1);

			key = key.replace(" ", "");
			if(key.contains("*")){
				key = key.replace("*", "");
			}
			LIWC.put(key, aff_class);
		}
	}
	
	public static int countWords(String text){
		int words     = 0;
	    String delimiters = ".,':;?{}[]=-+_!@#$%^&*() ";
	    StringTokenizer tokenizer = new StringTokenizer(text, delimiters);
	    
	    while(tokenizer.hasMoreTokens())
	    	words++;
	    
	    return words;
	}
	
	public static String getReadability(String text){
		//TODO Inserire chiamata all'indice scelto
		return String.valueOf(FleshIndex.getFleschGradeIndex(text));
	}
	
	public static String hasCodeSnippet(String text){
		String has_code = "no";
		if(text.contains("<code>"))
			has_code = "yes";
		
		return has_code;
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
	
	public static String getTopic(String tags){
		//TODO
		return "Selected topic";
	}
	
	public String SentiStrengthgetScore(String text){
		String score = sentiStrength.computeSentimentScores(text);
		String[] split_res = score.split(" ");
		String pos_score = split_res[0];
		String neg_score = split_res[1];
				
		return pos_score + "," + neg_score;
	}
	
	public String NLPgetScore(String text){
		String score = new String();
		String line = text.trim();
        
        if (line.length() > 0) {
        	Annotation annotation = tokenizer.process(line);
        	
        	pipeline.annotate(annotation);
            for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
          	  	score = score + "," + sentence.get(SentimentCoreAnnotations.ClassName.class);
            }
        }
          
		return score;
	}
	
	public String LIWCgetAffectiveClass(String word){
		return (String)LIWC.get(word);
	}
	
	public HashMap getAffClasses(String text){
		HashMap classes = new HashMap();
		classes.put("PREPS", 0); classes.put("NUMBER", 0); classes.put("AFFECT", 0); classes.put("POSEMO", 0); classes.put("POSFEEL", 0); classes.put("OPTIM", 0); classes.put("NEGEMO", 0); classes.put("ANX", 0); classes.put("ANGER", 0); classes.put("SAD", 0); classes.put("PRONOUN", 0); classes.put("COGMECH", 0); classes.put("CAUSE", 0); classes.put("INSIGHT", 0); classes.put("DISCREP", 0); classes.put("INHIB", 0); classes.put("TENTAT", 0); classes.put("CERTAIN", 0); classes.put("SENSES", 0); classes.put("SEE", 0); classes.put("HEAR", 0); classes.put("I", 0); classes.put("FEEL", 0); classes.put("SOCIAL", 0); classes.put("COMM", 0); classes.put("OTHREF", 0); classes.put("FRIENDS", 0); classes.put("FAMILY", 0); classes.put("HUMANS", 0); classes.put("TIME", 0);classes.put("PAST", 0); classes.put("PRESENT", 0); classes.put("WE", 0); classes.put("FUTURE", 0); classes.put("SPACE", 0); classes.put("UP", 0); classes.put("DOWN", 0); classes.put("INCL", 0); classes.put("EXCL", 0); classes.put("MOTION", 0); classes.put("OCCUP", 0); classes.put("SCHOOL", 0); classes.put("JOB", 0); classes.put("SELF", 0); classes.put("ACHIEVE", 0); classes.put("LEISURE", 0); classes.put("HOME", 0); classes.put("SPORTS", 0); classes.put("TV", 0); classes.put("MUSIC", 0); classes.put("MONEY", 0); classes.put("METAPH", 0); classes.put("RELIG", 0); classes.put("DEATH", 0); classes.put("YOU", 0); classes.put("PHYSCAL", 0); classes.put("BODY", 0); classes.put("SEXUAL", 0); classes.put("EATING", 0); classes.put("SLEEP", 0); classes.put("GROOM", 0); classes.put("SWEAR", 0); classes.put("NONFL", 0); classes.put("FILLERS", 0); classes.put("SIMILES", 0); classes.put("OTHER", 0); classes.put("NEGATE", 0); classes.put("ASSENT", 0); classes.put("ARTICLE", 0);
		
		//TODO Ciclo su testo tokenizzato
		if(LIWC.containsKey(text)){
			String aff_class = LIWCgetAffectiveClass(text);
			int c = (int)classes.get(aff_class);
			c++;
			classes.remove(aff_class);
			classes.put(aff_class, c);
		}
		
		return classes;
	}
	
	public String isAcceptedAnswer(String field){
		String acc;
		if(field.contains("None"))
			acc = "no";
		else
			acc = "yes";
		
		return acc;
	}
	
	public static int CSVgetColumn(String s_column, String inputFile) throws IOException{
		Reader in = new FileReader(inputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		int n_column = 0;
		CSVRecord record = records.iterator().next();
		
		int count = 0;
		Iterator it = record.iterator();
		while(it.hasNext()){
			String currentField = (String)it.next();
			if(currentField.equals(s_column))
				n_column = count;
			
			count++;
		}
		
		return n_column;
	}
	
	public void buildDataset(String inputFile, String outputFile) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(outputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		boolean first = true; 
		
		int post = this.CSVgetColumn("Post", inputFile);
		int user_quest_acc = this.CSVgetColumn("UsersQuestionsAccepted", inputFile);
		int user_answ_acc = this.CSVgetColumn("UsersAnswersAccepted", inputFile);
		int title = this.CSVgetColumn("PostTitle", inputFile);
		int body = this.CSVgetColumn("PostBody", inputFile);
		int tags = this.CSVgetColumn("PostTags", inputFile);
		int quest_up = this.CSVgetColumn("UpVotesQuest", inputFile);
		int quest_down = this.CSVgetColumn("DownVotesQuest", inputFile);
		int answ_up = this.CSVgetColumn("UpVotesAnsw", inputFile);
		int answ_down = this.CSVgetColumn("DownVotesAnsw", inputFile);
		int badges = this.CSVgetColumn("UsersBadges", inputFile);
		int accepted_answ = this.CSVgetColumn("PostAcceptedAnswerId", inputFile);
		
		
		
		for (CSVRecord record : records) {
			if(first == false){
				
				
				
				int q_up = 0, q_down = 0, a_up = 0, a_down = 0, q_score = 0, a_score = 0;
				int  title_length = 0, body_length = 0;
				String post_id = "";
				String post_title = "";
				String post_body = "";
				String body_readability = "";
				String code_snippet = "";
				String topic = "";
				String sentiment = "";
				String badge = "";
				String acc = "";
				String u_quest_acc = "";
				String u_answ_acc = "";
				HashMap aff_class = new HashMap();
				int count = 0;
				
				Iterator it = record.iterator();
				System.out.println("Lettura record...");
				while(it.hasNext()){
					String current_field = (String)it.next();
					
					if(count == post){
						System.out.println("Post...");
						//printer_csv.print(current_field);
						post_id = current_field;
					}else if(count == title){
						System.out.println("Title...");
						post_title = current_field;
						title_length = countWords(current_field);
					}else if(count == body){
						System.out.println("Body...");
						post_body = current_field;
						body_length = countWords(current_field);
						body_readability = getReadability(current_field);
						code_snippet = hasCodeSnippet(current_field);
						sentiment = SentiStrengthgetScore(current_field); //TODO SS o NLP ?
						aff_class = getAffClasses(current_field);
					}else if(count == quest_up){
						System.out.println("Quest UP...");
						q_up = Integer.valueOf(current_field);
					}else if(count == quest_down){
						System.out.println("Quest DOWN...");
						q_down = Integer.valueOf(current_field);
					}else if(count == answ_up){
						System.out.println("Answ UP...");
						a_up = Integer.valueOf(current_field);
					}else if(count == answ_down){
						System.out.println("Answ DOWN...");
						a_down = Integer.valueOf(current_field);
					}else if(count == tags){
						//TODO Topic
						System.out.println("Topic...");
						topic = "TOPICS";
					}else if(count == badges){
						System.out.println("Badges...");
						badge = current_field;
					}else if(count == accepted_answ){
						System.out.println("Acc Answ...");
						acc = isAcceptedAnswer(current_field);
					}else if(count == user_quest_acc){
						System.out.println("User Quest Acc...");
						u_quest_acc = current_field;
					}else if(count == user_answ_acc){
						System.out.println("User Answ Acc...");
						u_answ_acc = current_field;
					}

					count++;
				}
				System.out.println("Valori calcolati...");
				printer_csv.print(acc);
				printer_csv.print(post_id);
				printer_csv.print(post_title);
				printer_csv.print(post_body);
				printer_csv.print(Integer.valueOf(title_length));
				printer_csv.print(Integer.valueOf(body_length));
				printer_csv.print(body_readability);
				printer_csv.print(code_snippet);
				printer_csv.print(topic); //TODO
				printer_csv.print(Integer.valueOf(Math.abs(q_up-q_down)));
				printer_csv.print(Integer.valueOf(Math.abs(a_up-a_down)));
				printer_csv.print(u_quest_acc);
				printer_csv.print(u_answ_acc);
				printer_csv.print(badge);
				printer_csv.print(sentiment);
				printer_csv.print(aff_class); //TODO
				printer_csv.println();
				System.out.println("Record stampato...");
			}
			else{
				printer_csv.print("AcceptedAnswer");
				printer_csv.print("Post");
				printer_csv.print("PostTitle");
				printer_csv.print("PostBody");
				printer_csv.print("TitleLength");
				printer_csv.print("BodyLength");
				printer_csv.print("Readability");
				printer_csv.print("CodeSnippet");
				printer_csv.print("Topic");
				printer_csv.print("QuestionScore");
				printer_csv.print("AnswerScore");
				printer_csv.print("UsersQuestionsAccepted");
				printer_csv.print("UsersAnswersAccepted");
				printer_csv.print("UsersBadges");
				printer_csv.print("SentimentScore");
				printer_csv.print("PREPS"); printer_csv.print("NUMBER"); printer_csv.print("AFFECT"); printer_csv.print("POSEMO"); printer_csv.print("POSFEEL"); printer_csv.print("OPTIM"); printer_csv.print("NEGEMO"); printer_csv.print("ANX"); printer_csv.print("ANGER"); printer_csv.print("SAD"); printer_csv.print("PRONOUN"); printer_csv.print("COGMECH"); printer_csv.print("CAUSE"); printer_csv.print("INSIGHT"); printer_csv.print("DISCREP"); printer_csv.print("INHIB"); printer_csv.print("TENTAT"); printer_csv.print("CERTAIN"); printer_csv.print("SENSES"); printer_csv.print("SEE"); printer_csv.print("HEAR"); printer_csv.print("I"); printer_csv.print("FEEL"); printer_csv.print("SOCIAL"); printer_csv.print("COMM"); printer_csv.print("OTHREF"); printer_csv.print("FRIENDS"); printer_csv.print("FAMILY"); printer_csv.print("HUMANS"); printer_csv.print("TIME");printer_csv.print("PAST"); printer_csv.print("PRESENT"); printer_csv.print("WE"); printer_csv.print("FUTURE"); printer_csv.print("SPACE"); printer_csv.print("UP"); printer_csv.print("DOWN"); printer_csv.print("INCL"); printer_csv.print("EXCL"); printer_csv.print("MOTION"); printer_csv.print("OCCUP"); printer_csv.print("SCHOOL"); printer_csv.print("JOB"); printer_csv.print("SELF"); printer_csv.print("ACHIEVE"); printer_csv.print("LEISURE"); printer_csv.print("HOME"); printer_csv.print("SPORTS"); printer_csv.print("TV"); printer_csv.print("MUSIC"); printer_csv.print("MONEY"); printer_csv.print("METAPH"); printer_csv.print("RELIG"); printer_csv.print("DEATH"); printer_csv.print("YOU"); printer_csv.print("PHYSCAL"); printer_csv.print("BODY"); printer_csv.print("SEXUAL"); printer_csv.print("EATING"); printer_csv.print("SLEEP"); printer_csv.print("GROOM"); printer_csv.print("SWEAR"); printer_csv.print("NONFL"); printer_csv.print("FILLERS"); printer_csv.print("SIMILES"); printer_csv.print("OTHER"); printer_csv.print("NEGATE"); printer_csv.print("ASSENT"); printer_csv.print("ARTICLE");
				printer_csv.println();
				System.out.println("Header stampati...");
				first = false;
			}
				
			
			
		}
		printer_csv.close();
		System.out.println("Done");
	}
	
	public static void mullet(String inputFile) throws IOException{
		// Begin by importing documents from text to feature sequences
        ArrayList<Pipe> pipeList = new ArrayList<Pipe>();

        // Pipes: lowercase, tokenize, remove stopwords, map to features
        pipeList.add( new CharSequenceLowercase() );
        pipeList.add( new CharSequence2TokenSequence(Pattern.compile("\\p{L}[\\p{L}\\p{P}]+\\p{L}")) );
        pipeList.add( new TokenSequenceRemoveStopwords(new File("lib/mallet-2.0.7/stoplists/en.txt"), "UTF-8", false, false, false) );
        pipeList.add( new TokenSequence2FeatureSequence() );

        InstanceList instances = new InstanceList (new SerialPipes(pipeList));

        Reader fileReader = new InputStreamReader(new FileInputStream(new File(inputFile)), "UTF-8");
        instances.addThruPipe(new CsvIterator (fileReader, Pattern.compile("^(\\S*)[\\s,]*(\\S*)[\\s,]*(.*)$"),
                                               3, 2, 1)); // data, label, name fields

        // Create a model with 100 topics, alpha_t = 0.01, beta_w = 0.01
        //  Note that the first parameter is passed as the sum over topics, while
        //  the second is the parameter for a single dimension of the Dirichlet prior.
        int numTopics = 5;
        ParallelTopicModel model = new ParallelTopicModel(numTopics, 0.01/*1.0*/, 0.01);

        model.addInstances(instances);

        // Use two parallel samplers, which each look at one half the corpus and combine
        //  statistics after every iteration.
        model.setNumThreads(2);

        // Run the model for 50 iterations and stop (this is for testing only, 
        //  for real applications, use 1000 to 2000 iterations)
        model.setNumIterations(1000);
        model.estimate();

        // Show the words and topics in the first instance

        // The data alphabet maps word IDs to strings
        Alphabet dataAlphabet = instances.getDataAlphabet();
        
        FeatureSequence tokens = (FeatureSequence) model.getData().get(1).instance.getData();
        LabelSequence topics = model.getData().get(1).topicSequence;
        
        Formatter out = new Formatter(new StringBuilder(), Locale.US);
        for (int position = 0; position < tokens.getLength(); position++) {
            out.format("%s-%d ", dataAlphabet.lookupObject(tokens.getIndexAtPosition(position)), topics.getIndexAtPosition(position));
        }
        System.out.println(out);
        
        // Estimate the topic distribution of the first instance, 
        //  given the current Gibbs state.
        /*double[] topicDistribution = model.getTopicProbabilities(0);
        
        System.out.println("Topic 0" + Double.valueOf(topicDistribution[0]));
        System.out.println("Topic 1" + Double.valueOf(topicDistribution[1]));
        System.out.println("Topic 2" + Double.valueOf(topicDistribution[2]));
        System.out.println("Topic 3" + Double.valueOf(topicDistribution[3]));
        System.out.println("Topic 4" + Double.valueOf(topicDistribution[4]));
        */
        
        
        Reader in = new FileReader(inputFile);
        Writer outcsv = new FileWriter("mallet_topics.csv");
        Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
        CSVPrinter printer_csv = new CSVPrinter(outcsv, CSVFormat.DEFAULT);
        
        int i = 0;
        
        for (CSVRecord record : records) {
    		
        //for(int i=0; i<267; i++){
        	double[] topicDistribution = model.getTopicProbabilities(i);
        	
            printer_csv.print(record.get(0));
            for(int j=0; j<model.getNumTopics(); j++)
            	printer_csv.print(topicDistribution[j]);
            
            printer_csv.println();
        //}
        
        i++;
        }
        printer_csv.close();
        
        
	}
	
	/*
	 *  Analizza il file 'inputFile' (che deve essere in formato CSV) prendendo la colonna string_column
	 *  e scrive il risultato dell'analisi di SentiStrength nel file 'outputFile'
	 *  
	 *  	@param
	 *  		inputFile:		path del file di input in formato CSV
	 *  		outputFile:		path del file su cui scrivere i risultati
	 *  		body_column:	nome della colonna che contiene il testo da analizzare
	 */			
	public void analizeSentiStrengthCSV(String inputFile, String outputFile, String string_column) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(outputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		boolean first = true;
		int body_column = this.CSVgetColumn(string_column, inputFile);
		
		for (CSVRecord record : records) {
			if(first == false){
				// Riscrive file...
				Iterator it = record.iterator();
				while(it.hasNext()){
					String current_field = (String)it.next();
					printer_csv.print(current_field);
				}
				
				// ...aggiunge score SentiStrength
				String body = record.get(body_column);
				
				printer_csv.print(this.SentiStrengthgetScore(body).split(",")[0]);
				printer_csv.print(this.SentiStrengthgetScore(body).split(",")[1]);
				printer_csv.println();
			}
			else{
				first = false;
			}
				
			
			
		}
		printer_csv.close();
		System.out.println("Done");
	}
	
	
	public void analizeNLPCSV(String inputFile, String outputFile, String string_column) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(outputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		boolean first = true;
		int body_column = this.CSVgetColumn(string_column, inputFile);
		
	    
		for (CSVRecord record : records) {
			if(first == false){
				// Riscrive file...
				Iterator it = record.iterator();
				while(it.hasNext()){
					String current_field = (String)it.next();
					printer_csv.print(current_field);
				}
				
				// ...aggiunge score NLP
				String body = record.get(body_column);
				String[] scores = this.NLPgetScore(body).split(",");
				
			    for(int i = 0; i < scores.length; i++)
			    	printer_csv.print(scores[i]);
			    
				printer_csv.println();
			}
			else{
				first = false;
			}	
		}
		printer_csv.close();
		System.out.println("Done");
	}
	
	/*
	 * Prende in input il file CSV contenente tutti i post
	 */
	public void listTagsStatistics(String inputFile) throws IOException{
		Reader in = new FileReader(inputFile);
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		LinkedList<String> tags = new LinkedList<String>();
		
		int tags_column = 0;
		int posttype_column = 0;
		
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
				
				String post_type = record.get(posttype_column);
				String field_tags = record.get(tags_column);
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
			else{
				int count = 0;
				Iterator it = record.iterator();
				while(it.hasNext()){
					String currentField = (String)it.next();
					if(currentField.equals("Tags"))
						tags_column = count;
					else if(currentField.equals("PostTypeId"))
						posttype_column = count;
					
					count++;
				}
				
				first = false;
			}
		}
		
		average = (float)part_value/(float)num_records;
		tags_p_quest = (float)part_value/(float)quest;
		
		Collections.sort(tags);
		Writer out = new FileWriter(inputFile.replace(".csv", ".txt"));
		out.write("Tags identified:\n");
		Iterator<String> it = tags.iterator();
		while(it.hasNext()){
			num_tags++;
			out.write("\t"+it.next()+"\n");
		}
		
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
		System.out.println("Done");
	}
	
	/*
	 * Riscrive il file dato in input con il campo Tags ripulito dai caratteri "<" ">" 
	 */
	public void cleanTagsCSV(String inputFile, String tags_field) throws IOException{
		Reader in = new FileReader(inputFile);
		Writer out = new FileWriter(inputFile.replace(".csv", "_clean.csv"));
		Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(in);
		CSVPrinter printer_csv = new CSVPrinter(out, CSVFormat.DEFAULT);
		
		boolean first = true;
		int tags_column = 0;
		
		for (CSVRecord record : records) {
			if(first == false){
				// Riscrive file...
				Iterator it = record.iterator();
				int count = 0;
				while(it.hasNext()){
					String current_field = (String)it.next();
					
					if(count == tags_column){
						if(!current_field.equals("None")){
							String tags_cleaned = current_field.replace(">", " ").replace("<", "");
							printer_csv.print(tags_cleaned);
						}else{
							printer_csv.print(current_field);
						}
					}else{
						printer_csv.print(current_field);
					}
					
					count++;
				}
				printer_csv.println();
				
			}
			else{
				int count = 0;
				Iterator it = record.iterator();
				while(it.hasNext()){
					String currentField = (String)it.next();
					if(currentField.equals(tags_field))
						tags_column = count;
					
					count++;
				}
				first = false;
			}
			
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
		
		
		//App app = new App();
		//app.cleanTagsCSV("downloaded.csv", "Tags");
		//app.listTagsStatistics("it_posts.csv");
		//app.analizeSentiStrengthCSV("ac_questions.csv", "ac_questions_ss2.csv", "Body");
		//app.analizeNLPCSV("ac_questions.csv", "ac_questions_ss_nlp.csv", "Body");
		//app.analizeLines(input_file_dir + "input.txt", output_file_dir + "output.txt");
		//app.analizeOneLine(input_file_dir + "input.txt", 1);
		//app.buildDataset("result-set.csv", "logit_regr.csv");
		App.mullet("tags.csv");
		
		
		/*String prova_1 = "The Flesch Reading Ease Score indicates on a scale of 0 to 100 the difficulty of comprehending a document. A score of 100 indicates an extremely simple document, while a score of 0 would describe a very complex document. A Flesch Reading Ease Score in the range of 40–50 would correspond to a relatively complex document that might score a 12 as its Flesch-Kincaid Grade Level. The Flesch Reading Ease Score can be calculated by using the following equation.";
		String prova_2 = "Technically R is an expression language with a very simple syntax. It is case sensitive as are most UNIX based packages, so A and a are different symbols and would refer to different variables. The set of symbols which can be used in R names depends on the operating system and country within which R is being run (technically on the locale in use).";
		String prova_3 = "Elementary commands consist of either expressions or assignments. If an expression is given as a command, it is evaluated, printed (unless specifically made invisible), and the value is lost. An assignment also evaluates an expression and passes the value to a variable but the result is not automatically printed.";
		String prova_4 = "Alternatively, the Emacs text editor provides more general support mechanisms (via ESS, Emacs Speaks Statistics) for working interactively with R.";
		String prova_5 = "It is recommended that you should use separate working directories for analyses conducted with R. It is quite common for objects with names x and y to be created during an analysis. Names like this are often meaningful in the context of a single analysis, but it can be quite hard to decide what they might be when the several analyses have been conducted in the same directory.";
		FleshIndex.calculate(prova_1);
		FleshIndex.calculate(prova_2);
		FleshIndex.calculate(prova_3);
		FleshIndex.calculate(prova_4);
		FleshIndex.calculate(prova_5);*/
		
		//System.out.println(app.LIWCgetAffectiveClass("thank"));
	}

}
