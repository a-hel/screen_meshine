
/**
 * Script based on GenericBatchUser.java from the MTI examples
**/


import java.io.*;
import java.util.Arrays;
import gov.nih.nlm.nls.skr.*;

public class Indexer
{
    static String defaultCommand = "MTI -opt1L_DCMS -E";


    /** print information about server options */
    public static void printHelp() 
    {
      System.out.println("usage: Indexer username password e-mail");
      System.out.println("  output_file input_file_1 input_file_2 input_file_n ");  
    }


    public static void main(String args[])
    {
        String userName = null;
        String password = null;
        String emailAddress = null;
        String outFile = null;
        String inFiles[];
        
        if (args.length < 1) {
          printHelp();
          System.exit(1);
          } else if (args.length < 4){
            System.out.println("Not enough arguments.");
            printHelp();
            System.exit(1);

          }
        userName = args[0];
        password = args[1];
        emailAddress = args[2];
        outFile = args[3];
        inFiles = Arrays.copyOfRange(args, 4, args.length);

        try
        {
          File res_file = new File(outFile);
          res_file.createNewFile();
          FileWriter writer = new FileWriter(res_file);

          for (int i=0; i<inFiles.length; i++){
            System.out.println("Processing file: " + inFiles[i]);

            GenericObject myGenericObj = new GenericObject(userName, password);
            myGenericObj.setField("Email_Address", emailAddress);
            myGenericObj.setFileField("UpLoad_File", inFiles[i]);
            myGenericObj.setField("Batch_Command", "MTI -opt1L_DCMS -E");
            myGenericObj.setField("BatchNotes", "SKR Web API test");
            myGenericObj.setField("SilentEmail", true);

            // Submit the job request
            String results = myGenericObj.handleSubmission();
            writer.write("#" + inFiles[i] + "\n");
            writer.write(results);

             
        } // for
        writer.flush();
        writer.close();
      } catch (IOException ex) {
               System.err.println("");
               System.err.print("There is a problem with File IO");
               System.err.println("");
               System.err.println("Trace:");
               ex.printStackTrace();
      } catch (RuntimeException ex) {
               System.err.println("");
               System.err.print("An ERROR has occurred while processing your");
               System.err.println(" request, please review any");
               System.err.print("lines beginning with \"Error:\" above and the");
               System.err.println(" trace below for indications of");
               System.err.println("what may have gone wrong.");
               System.err.println("");
               System.err.println("Trace:");
               ex.printStackTrace();
      } // catch
   } // main
} // class GenericBatch
