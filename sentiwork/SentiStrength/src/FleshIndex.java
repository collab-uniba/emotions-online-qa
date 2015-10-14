// The Flesch Index
// Daniel Shiffman
// Programming from A to Z, Spring 2006

import java.io.*;

import java.util.StringTokenizer;

public class FleshIndex {
  public static void calculate (String content) throws IOException {
    
    int syllables = 0;
    int sentences = 0;
    int words     = 0;

    String delimiters = ".,':;?{}[]=-+_!@#$%^&*() ";
    StringTokenizer tokenizer = new StringTokenizer(content,delimiters);
    //go through all words
    while (tokenizer.hasMoreTokens())
    {
      String word = tokenizer.nextToken();
      syllables += countSyllables(word);
      words++;
    }
    sentences = countSentences(content);
    
    //calculate flesch index
    calcfinal float f1 = (float) 206.835;
    final float f2 = (float) 84.6;
    final float f3 = (float) 1.015;
    float r1 = (float) syllables / (float) words;
    float r2 = (float) words / (float) sentences;
    float flesch = f1 - (f2*r1) - (f3*r2);
    
    final float f4 = (float) 0.39;
    final float f5 = (float) 11.8;
    final float f6 = (float) 15.59;
    float fleschgrade = (f4*r2) + (f5*r1) - f6;

    //Write Report
    String report = "";
    
    report += "Total Syllables: " + syllables + "\n";
    report += "Total Words    : " + words + "\n";
    report += "Total Sentences: " + sentences + "\n";
    report += "Flesch Ease Index   : " + flesch + "\n";
    report += "Flesch Grade Index   : " + fleschgrade + "\n";
    System.out.println(report);

    
  }

/*
public static float getCLI (String text){
// metodo per calcolare indice di readability 
// Coleman Liaw Index

	int sentence = 0;
	int words = 0;
	int charactersL = 0;
	int charactsS = 0;

	String delimmiters = ".,':;?{}[]=-+_!@#$%^&*() ";
	StringTokenizer tokenizer = new StringTokenizer(text, delimiters);

	for (int i = 1; i <= 100; i++)
	    {
    		String word = tokenizer.nextToken();
		charactersL += countCharacters(word);
    		}
    		int L = charactersL/100; //media caratteri in 100 parole
	//manca calcolo S, media del numero di frasi per 100 parole
	
	for (int j = 1; j <= 100; j++)
	    {
    		String word = tokenizer.nextToken();
		charactersS += countCharacters(word);
    		}
    		int subS = charactersS+100
    		String subStr = subStr.substring(0,subS);
	    	sentences = countSentences(subStr);
	    
	    int S = sentences/100; //numero di frasi medio ogni 100 parole

	    //calculate Coleman Liaw Index
	    final float f1 = (float) 0.588;
	    final float f2 = (float) 0.296;
	    final float f3 = (float) 15.8;
	    
	    float CLI = (f1 * L) - (f2 * S) - f3;
	    
	return CLI;
}
*/



public static float getARI (String text){
	
	int sentence = 0;
	int words = 0;
	int characters = 0;
	
	String delimmiters = ".,':;?{}[]=-+_!@#$%^&*() ";
	StringTokenizer tokenizer = new StringTokenizer(text, delimiters);
	while (tokenizer.hasMoreTokens())
	{
		String word = tokenizer.nextToken();
		characters += countCharacters(word);
		words++;
	}
    sentences = countSentences(text);
	    
	    //calculate Automated Reading Index
	    final float f1 = (float) 4.71;
	    final float f2 = (float) 0.5;
	    final float f3 = (float) 21.43;
	    float r1 = (float) characters / (float) words;
	    float r2 = (float) words / (float) sentences;
	    float ARI = (f1 * r1) + (f2 * r2) - f3;
	    
	return ARI;
}

//conta caratteri in una parola
public static int countCharacters(String word) {
	
    int ch = word.length();
    return ch;
}


public static int countWords(String content){
	//conta le parole in un testo
    int words = 0;	
    String wordDelim = ".,':;?{}[]=-+_!@#$%^&*() ";
    StringTokenizer wordTokenizer = new StringTokenizer(content,wordDelim);
    words = wordTokenizer.countTokens();
    
    return words;
	
}


public static int countSentences(String content){
	//conta le frasi in un testo
    int sentences = 0;	
    String sentenceDelim = ".:;?!";
    StringTokenizer sentenceTokenizer = new StringTokenizer(content,sentenceDelim);
    sentences = sentenceTokenizer.countTokens();
    
    return sentences;
	
}
  public static float getFleschEaseIndex(String text){

	    int syllables = 0;
	    int sentences = 0;
	    int words     = 0;

	    String delimiters = ".,':;?{}[]=-+_!@#$%^&*() ";
	    StringTokenizer tokenizer = new StringTokenizer(text,delimiters);
	    //go through all words
	    while (tokenizer.hasMoreTokens())
	    {
	      String word = tokenizer.nextToken();
	      syllables += countSyllables(word);
	      words++;
	    }
	    //look for sentence delimiters
	       sentences = countSentences(text);
 
	    //calculate flesch index
	    final float f1 = (float) 206.835;
	    final float f2 = (float) 84.6;
	    final float f3 = (float) 1.015;
	    float r1 = (float) syllables / (float) words;
	    float r2 = (float) words / (float) sentences;
	    float flesch = f1 - (f2*r1) - (f3*r2);
	    
	    return flesch;
  }

  public static float getFleschGradeIndex(String text){

	    int syllables = 0;
	    int sentences = 0;
	    int words     = 0;

	    String delimiters = ".,':;?{}[]=-+_!@#$%^&*() ";
	    StringTokenizer tokenizer = new StringTokenizer(text,delimiters);
	    //go through all words
	    while (tokenizer.hasMoreTokens())
	    {
	      String word = tokenizer.nextToken();
	      syllables += countSyllables(word);
	      words++;
	    }
	    //look for sentence delimiters
	       sentences = countSentences(text);
 
	    //calculate flesch index

	    final float f4 = (float) 0.39;
	    final float f5 = (float) 11.8;
	    final float f6 = (float) 15.59;
	    float r1 = (float) syllables / (float) words;
	    float r2 = (float) words / (float) sentences;
	    float fleschgrade = (f4*r2) + (f5*r1) - f6;
	    
	    return fleschgrade;
}
  
// A method to count the number of syllables in a word
// Pretty basic, just based off of the number of vowels
// This could be improved
public static int countSyllables(String word) {
    int      syl    = 0;
    boolean  vowel  = false;
    int      length = word.length();

    //check each word for vowels (don't count more than one vowel in a row)
    for(int i=0; i<length; i++) {
      if        (isVowel(word.charAt(i)) && (vowel==false)) {
        vowel = true;
        syl++;
      } else if (isVowel(word.charAt(i)) && (vowel==true)) {
        vowel = true;
      } else {
        vowel = false;
      }
    }

    char tempChar = word.charAt(word.length()-1);
    //check for 'e' at the end, as long as not a word w/ one syllable
    if (((tempChar == 'e') || (tempChar == 'E')) && (syl != 1)) {
      syl--;
    }
    return syl;
}

//check if a char is a vowel (count y)
public static boolean isVowel(char c) {
    if      ((c == 'a') || (c == 'A')) { return true;  }
    else if ((c == 'e') || (c == 'E')) { return true;  }
    else if ((c == 'i') || (c == 'I')) { return true;  }
    else if ((c == 'o') || (c == 'O')) { return true;  }
    else if ((c == 'u') || (c == 'U')) { return true;  }
    else if ((c == 'y') || (c == 'Y')) { return true;  }
    else                               { return false; }
  }
}
