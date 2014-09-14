import uk.ac.wlv.sentistrength.*;

import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;


public class Sentiment {
	
	public Sentiment() {
		// TODO Auto-generated constructor stub
		super();
		
	}
	
	public String SentiStrengthgetScore(String text){
		SentiStrength sentiStrength = new SentiStrength();
		String ssthInitialisation[] = {"sentidata", "lib/SentiStrength_Data/", "explain"};
		sentiStrength.initialise(ssthInitialisation);
		String score = sentiStrength.computeSentimentScores(text);
		String[] split_res = score.split(" ");
		String pos_score = split_res[0];
		String neg_score = split_res[1];
				
		//return pos_score + "," + neg_score;
		return score;
	}

	public String NLPgetScore(String text){
		Properties pipelineProps = new Properties();
	    //pipelineProps.setProperty("ssplit.eolonly", "true");
	    pipelineProps.setProperty("annotators", "tokenize,pos,cleanxml,parse,sentiment");
	    pipelineProps.setProperty("enforceRequirements", "false");
	    
	    Properties tokenizerProps = new Properties();
	    tokenizerProps.setProperty("annotators", /*"tokenize, ssplit"*/"tokenize,cleanxml,ssplit,"+/*pos,lemma,*/"parse,sentiment");
	    System.out.println("Annotator loaded");
	    StanfordCoreNLP tokenizer = new StanfordCoreNLP(tokenizerProps);
	    StanfordCoreNLP pipeline = new StanfordCoreNLP(pipelineProps);
		
	    
	    
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
}
