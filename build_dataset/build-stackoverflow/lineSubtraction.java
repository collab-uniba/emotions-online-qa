/*
* Script per eseguire la sottrazione di righe tra due csv
* Prende in input tre parametri: File di base, File con le righe da sottrarre e File di output 
*
* esempio di utilizzo:
* java lineSubtraction /mnt/vdb1/emotions-online-qa/build_dataset/fileBase.csv /mnt/vdb1/emotions-online-qa/build_dataset/fileDaSottrarre.csv /mnt/vdb1/emotions-online-qa/build_dataset/result.csv
*
*/

import java.io.*;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;
import java.lang.*;
import java.lang.Object;

import java.io.Serializable;

public class lineSubtraction{


	public static void main(String[] args) {

        try {

            //carica gli id da rimuovere

            BufferedReader reader = new BufferedReader(new FileReader(args[0]));

            Set<String> ids = new HashSet<>();

            String line;
			String line1;
            String[] split;
			String[] split1;
            while (reader.ready()) {
				line1 = reader.readLine();
				split1 = line1.split(";");
                ids.add(split1[0]);

            }

            reader.close();

            reader = new BufferedReader(new FileReader(args[1]));

            BufferedWriter writer = new BufferedWriter(new FileWriter(args[2]));

            //lascia questo if se il file di input ha l'header csv che devi copiare pari pari nell'output

            if (reader.ready()) {

                writer.append(reader.readLine());

                writer.newLine();

            }

            int c = 0;

            while (reader.ready()) {
	        
                line = reader.readLine();
		
                split = line.split(";"); //cambia il caratter di split
		
                if (ids.contains(split[0])) { //scrive se l'id NON è nel set

                    writer.append(line);

                    writer.newLine();

                }

                c++;

                if (c % 10000 == 0) {

                    System.out.print(".");

                    if (c % 1000000 == 0) {

                        System.out.println(c);

                    }

                }

            }

            writer.close();

            reader.close();

        } catch (IOException ex) {

            Logger.getLogger(lineSubtraction.class.getName()).log(Level.SEVERE, null, ex);

        }

    }
}
