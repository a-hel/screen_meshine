/*
===========================================================================
*
*                            PUBLIC DOMAIN NOTICE                          
*               National Center for Biotechnology Information
*         Lister Hill National Center for Biomedical Communications
*                                                                          
*  This software is a "United States Government Work" under the terms of the
*  United States Copyright Act.  It was written as part of the authors' official
*  duties as a United States Government contractor and thus cannot be
*  copyrighted.  This software is freely available to the public for use. The
*  National Library of Medicine and the U.S. Government have not placed any
*  restriction on its use or reproduction.  
*                                                                          
*  Although all reasonable efforts have been taken to ensure the accuracy  
*  and reliability of the software and data, the NLM and the U.S.          
*  Government do not and cannot warrant the performance or results that    
*  may be obtained by using this software or data. The NLM and the U.S.    
*  Government disclaim all warranties, express or implied, including       
*  warranties of performance, merchantability or fitness for any particular
*  purpose.                                                                
*                                                                          
*  Please cite the authors in any work or product based on this material.   
*
===========================================================================
*/

/**
 * Example program for submitting a new Generic Batch with Validation job
 * request to the Scheduler to run. You will be prompted for your username and
 * password and if they are alright, the job is submitted to the Scheduler and
 * the results are returned in the String "results" below.
 *
 * This example shows how to setup a basic Generic Batch with Validation job
 * with a small file (sample.txt) with ASCII MEDLINE formatted citations as
 * input data. You must set the Email_Address variable and use the UpLoad_File
 * to specify the data to be processed.  This example also shows the user
 * setting the SilentEmail option which tells the Scheduler to NOT send email
 * upon completing the job.
 *
 * This example is set to run the MTI (Medical Text Indexer) program using
 * the -opt1L_DCMS and -E options. You can also setup any environment variables
 * that will be needed by the program by setting the Batch_Env field.
 * The "-E" option is required for all of the various SKR tools (MetaMap,
 * SemRep, and MTI), so please make sure to add the option to your command!
 * 
 * @author	Jim Mork
 * @version	1.0, September 18, 2006
**/


import java.io.*;
import java.util.Arrays;
import gov.nih.nlm.nls.skr.*;

public class JobSubmitter
{
    static String defaultCommand = "MTI -opt1L_DCMS -E";


    /** print information about server options */
    public static void printHelp() 
    {
      System.out.println("usage: JobSubmitter username password e-mail");
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