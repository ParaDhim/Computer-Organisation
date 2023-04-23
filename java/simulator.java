import java.util.*;
import java.io.*;


public class onlyparctice {
    
    static int cp=0;

    static boolean helper=false;
    static String[] sim=new String[256];
    static Hashtable<String,String> forreg=new Hashtable<>();
    static Hashtable<String,String> varhelper=new Hashtable<>();
    
    static ArrayList<String> varhelperlist=new ArrayList<>();

    static ArrayList<Integer> majboori=new ArrayList<>();
    
    static ArrayList<Integer> majboori2=new ArrayList<>();
    
    static int cycles=0;
    
    static String last="";
    public static void main(String[] args) throws IOException{
        
        Scanner sc=new Scanner(System.in); 
        

        forreg.put("R0", "0000000000000000");
        forreg.put("R1", "0000000000000000");
        forreg.put("R2", "0000000000000000");
        forreg.put("R3", "0000000000000000");
        forreg.put("R4", "0000000000000000");
        forreg.put("R5", "0000000000000000");
        forreg.put("R6", "0000000000000000");
        forreg.put("FLAGS", "0000000000000000");
        
        String[] reg= {"R0","R1","R2","R3","R4","R5","R6","FLAGS"};
        
        int i=0;
        int varcount=0;
        int cycles=0;
        while (true) {
            String s=sc.nextLine();
            sim[i]=s;
            
            if ((s.substring(0,5).equals("00100") || s.substring(0,5).equals("00101")) && !varhelper.contains(s.substring(8))) {
                varhelper.put(s.substring(8),intstantvariable16("0"));
                varhelperlist.add(s.substring(8));
            }
            if (s.equals("1001100000000000")) {
                break;
            }
            i++;
            majboori2.add(cycles++);
            
        }
        majboori2.add(cycles++);
        i++;
        
//        System.out.println(varhelper);
        
        Print(i,reg);


    }
    
    
//0001000000000010
//0001000100000011
//0000000011000001
//1001100000000000
    
    public static String whichreg(String s) {
        if (s.equals("000")) {
            return "R0";
        }
        else if (s.equals("001")) {
            return "R1";
        }
        else if (s.equals("010")) {
            return "R2";
        }
        else if (s.equals("011")) {
            return "R3";
        }
        else if (s.equals("100")) {
            return "R4";
        }
        else if (s.equals("101")) {
            return "R5";
        }
        else if (s.equals("110")) {
            return "R6";
        }
        else if (s.equals("111")) {
            return "FLAGS";
        }
        else {
            System.out.print("TYPO ERROR");
            System.exit(0);
            return "";
        }
    }
    
    public static int convbtoI(String S){
        int g=Integer.parseInt(S,2);
        return g;
    }
    
    public static String convItoB(int S){
        String R = Integer.toBinaryString(S);
        return R;
    }
    
    public static void setflag() {
        if (last.equals("01110")) {
            forreg.put("FLAGS", intstantvariable16("0"));
        }
    }
    
    public static void func(String s){
        if(s.substring(0,5).equals("00000")){   // add Type{A} opcode(5) unused(2) reg1(3) reg2(3) reg3(3); 
            
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));

            String ans=intstantvariable16(convItoB(a+b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if ((s.substring(0,5).equals("00001"))){   // sub Type{A} opcode(5) unused(2) reg1(3) reg2(3) reg3(3);
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            String ans=intstantvariable16(convItoB(a-b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("00010"))){    // mov immediate Type{B} opcode(5) reg1(3) Immediate value(8);
            String a=whichreg(s.substring(5,8));

            String ans=intstantvariable16(s.substring(8));

            forreg.put(a, ans);
            setflag();
        }
        else if((s.substring(0,5).equals("00011"))){   // mov register Type{C} opcode(5) unused(5) reg1(3) reg2(3);
            forreg.put(whichreg(s.substring(10,13)), forreg.get(whichreg(s.substring(13,16))));
            setflag();
        }
        else if((s.substring(0,5).equals("00100"))){   // load Type{D} opcode(5) reg1(3) Variable line(8);
            forreg.put(whichreg(s.substring(5,8)), varhelper.get(s.substring(8)));
            majboori.add(convbtoI(s.substring(8)));
            majboori2.add(cycles);
            setflag();
        }
        else if((s.substring(0,5).equals("00101"))){   // store Type{D} opcode(5) reg1(3) Variable line(8);
            varhelper.put(s.substring(8), forreg.get(whichreg(s.substring(5,8))));
            majboori2.add(cycles);
            majboori.add(convbtoI(s.substring(8)));
            setflag();
        }
        else if((s.substring(0,5).equals("00110"))){   // mul Type{A} opcode(5) unused(2) reg1(3) reg2(3) reg3(3);
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            String ans=intstantvariable16(convItoB(a*b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("00111"))){   // Div Type{C} opcode(5) unused(5) reg1(3) reg2(3);
            int a=convbtoI(s.substring(10,13));
            int b=convbtoI(s.substring(13,16));
            forreg.put("R0", intstantvariable16(convItoB(a/b)));
            forreg.put("R0", intstantvariable16(convItoB(a%b)));
            setflag();
        }
        else if((s.substring(0,5).equals("01000"))){   // rs immediate Type{B} opcode(5) reg1(3) Immediate value(8);
            String binroot=whichreg(s.substring(5,8));
            int a=convbtoI(forreg.get(whichreg(s.substring(5,8))));
            int b=convbtoI(s.substring(8));
            
            String ans=intstantvariable16(convItoB(a+b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01001"))){   // ls immediate Type{B} opcode(5) reg1(3) Immediate value(8);
            String binroot=whichreg(s.substring(5,8));
            int a=convbtoI(forreg.get(whichreg(s.substring(5,8))));
            int b=convbtoI(s.substring(8));
        
            String ans=intstantvariable16(convItoB(a-b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01010"))){   // xor { opcode (5 bits) , unused (2 bits) , reg1 (3 bits) , reg2 (3 bits) , reg3 (3 bits) }
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            String ans=convItoB(a^b);
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01011"))){   // or  { opcode (5 bits) , unused (2 bits) , reg1 (3 bits) , reg2 (3 bits) , reg3 (3 bits) }
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            String ans=intstantvariable16(convItoB(a|b));
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01100"))){    // and  { opcode (5 bits) , unused (2 bits) , reg1 (3 bits) , reg2 (3 bits) , reg3 (3 bits) }
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            String ans=convItoB(a&b);
            
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01101"))){    // not { opcode (5 bits) , unused (5 bits) , reg1 (3 bits) , reg2 (3 bits)  }
            String binroot=whichreg(s.substring(7,10));
            int a=convbtoI(forreg.get(s.substring(10,13)));
            String ans=intstantvariable16(convItoB(~a));
            forreg.put(binroot,ans);
            setflag();
        }
        else if((s.substring(0,5).equals("01110"))){    //cmp {opcode (5 bits) , unused(5 bits) , reg1 (3 bits) , reg2 (3 bits) }
            int a=convbtoI(forreg.get(whichreg(s.substring(10,13))));
            int b=convbtoI(forreg.get(whichreg(s.substring(13,16))));
            if(a==b){
                forreg.put("FLAGS", "0000000000000001");
            } 
            else if(a>b){
                forreg.put("FLAGS", "0000000000000010");
            }
            else {
                forreg.put("FLAGS", "0000000000000100");
            }
        }
        else if((s.substring(0,5).equals("01111"))){    //Unconditional jump (jmp) {opcode(5 bits) ,unused(3 bits) ,Memory Address(8 bits)}
            System.out.print(s.substring(8));
            helper=true;
            setflag();
        }
        else if((s.substring(0,5).equals("10000"))){    //Jump If Less than(jlt) {opcode(5 bits) ,unused(3 bits) ,Memory Address(8 bits)}
            if (forreg.get("FLAGS").equals("0000000000000100")) {
                System.out.print(s.substring(8));
                helper=true;
            }
            setflag();
        }
        else if((s.substring(0,5).equals("10001"))){    //Jump If Greater Than(jgt) {opcode(5 bits) ,unused(3 bits) ,Memory Address(8 bits)}
            if (forreg.get("FLAGS").equals("0000000000000010")) {
                System.out.print(s.substring(8));
                helper=true;
            }
            setflag();
        }
        else if((s.substring(0,5).equals("10010"))){    //Jump If Equal(je) {opcode(5 bits) ,unused(3 bits) ,Memory Address(8 bits)}
            if (forreg.get("FLAGS").equals("0000000000000001")) {
                System.out.print(s.substring(8));
                helper=true;
            }
            setflag();
        }

    }
    
    
    public static String intstantvariable8(String a) {
        int c=a.length();
        int x=8-c;
        String s="";
        for(int i=0;i<x;i++){
            s=s+"0";
        }
        s=s+a;
        return s;
    }
    
    public static String intstantvariable16(String a) {
        int c=a.length();
        int x=16-c;
        String s="";
        for(int i=0;i<x;i++){
            s=s+"0";
        }
        s=s+a;
        return s;
    }
    
    public static void Print(int i,String[] reg) throws IOException {
        
        for (int j=0;j<i;j++) {
            
//          if ((sim[j].substring(0,5).equals("01110")) && (!sim[j+1].substring(0,5).equals("01111") || !sim[j+1].substring(0,5).equals("10000") || !sim[j+1].substring(0,5).equals("10001") || !sim[j+1].substring(0,5).equals("10010"))) {
//              forreg.put("FLAGS", intstantvariable16("0"));
//          }
            
            func(sim[j]);
            if (helper==false) {
                majboori.add(cp);
                System.out.print(intstantvariable8(convItoB(cp))+" ");
            }
            helper=false;
            cp++;
            
            
            for (int k=0;k<reg.length;k++) {
                System.out.print(forreg.get(reg[k])+" ");
            }
            
            
            last=sim[j].substring(0,5);
            System.out.println();
            
        }    
        
//        System.out.println(varhelper);
        
        for (int j=0;j<varhelper.size();j++) {
            String g=varhelperlist.get(j);
            sim[i]=varhelper.get(g);
            i++;
        }
        
        for (int j=0;j<sim.length;j++) {
            if (sim[j]==null) {
                System.out.println("0000000000000000");
            }
            
            else {
                System.out.println(sim[j]);
            }
        }
//        System.out.println(majboori.size());
//        System.out.println(majboori2.size());
        
        FileWriter writer = new FileWriter("output.txt"); 
        for(int s=0;s<majboori.size();s++) {
            writer.write(majboori.get(s) + " "+ majboori2.get(s) + System.lineSeparator());
            
        }
        writer.close();

        
        
    }


}