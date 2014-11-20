package stemming;

import java.util.StringTokenizer;

import org.tartarus.snowball.SnowballStemmer;


public class Snowball {

	public Snowball(){
		super();
	}
	
	public static StringTokenizer split_words(String text){
		//int words     = 0;
	    //String delimiters = ".,':;?{}[]=-+_!@#$%^&*() ";
		String delimiters = ".,':;?{}[]=+_!@#$%^&*() "; // Mallet-difftoken
	    StringTokenizer tokenizer = new StringTokenizer(text, delimiters);
	    
	    return tokenizer;
	}
	
	public static String extract_stem(String input) throws ClassNotFoundException, InstantiationException, IllegalAccessException {
		Class stemClass = Class.forName("org.tartarus.snowball.ext.englishStemmer");
		SnowballStemmer stemmer = (SnowballStemmer) stemClass.newInstance();
		int repeat = 1;
		stemmer.setCurrent(input.toString());
	    for (int i = repeat; i != 0; i--) {
		stemmer.stem();
	    }
	    return stemmer.getCurrent();
	}
	
	public static String extract_stem_corpus(String corpus) throws ClassNotFoundException, InstantiationException, IllegalAccessException{
		StringTokenizer splitted_corpus = split_words(corpus);
		String stemmed_corpus = "";
		String curr_word = "";
		String curr_stem = "";
		
		while(splitted_corpus.hasMoreTokens()){
			
			curr_word = splitted_corpus.nextToken();
			curr_stem = extract_stem(curr_word);
			stemmed_corpus = stemmed_corpus + curr_stem + " ";
			
			//System.out.println("Word: " + curr_word);
			//System.out.println("Stem: " + curr_stem);
			//System.out.println();
		}
		
		return stemmed_corpus;
	}
	
	/*public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException {
		// TODO Auto-generated method stub

		Snowball s = new Snowball();
		String corpus = "On my machine (XP, 64) the ASP.net worker process (w3wp.exe) always launches with 5.5GB of Virtual Memory reserved. This happens regardless of the web application it's hosting (it can be anything, even an empty web page in aspx). This big old chunk of virtual memory is reserved at the moment the process starts, so this isn't a gradual memory \"leak\" of some sort. Some snooping around with windbg shows that the memory is question is Private, Reserved and RegionUsageIsVAD, which indicates it might be the work of someone calling VirtualAlloc. It also shows that the memory in question is allocated/reserved in 4 big chunks of 1GB each and a several smaller ones (1/4GB each).";
		String corpus2 = "Attaching a debugger to the process prior to the memory allocation is tricky, because w3wp.exe is a process launched by svchost.exe (that is, IIS/ASP.Net filter) and if I try to launch it myself in order to debug it it just closes down without all this profuse memory reservation. Also, the command line parameters are invalid if I resuse them (which makes sense because it's a pipe created by the calling process).";
		System.out.println(Snowball.extract_stem_corpus(corpus2));
		//System.out.println(s.extract_stem("classes"));
	}*/

}
