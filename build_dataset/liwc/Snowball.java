import org.tartarus.snowball.SnowballStemmer;


public class Snowball {

	public static String stem(String input) throws Throwable{
		Class stemClass = Class.forName("org.tartarus.snowball.ext.englishStemmer");
		SnowballStemmer stemmer = (SnowballStemmer) stemClass.newInstance();
		int repeat = 1;
		stemmer.setCurrent(input.toString());
	    for (int i = repeat; i != 0; i--) {
		stemmer.stem();
	    }
	    return stemmer.getCurrent();
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
