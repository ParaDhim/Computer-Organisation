import java.util.*;
import java.io.*;

public class onlyparctice {
    static ArrayList<String> help = new ArrayList<>();
    static ArrayList<String> bin = new ArrayList<>();
    static ArrayList<String[]> helper2 = new ArrayList<>();
    static Hashtable<String, Integer> dict = new Hashtable<>();

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int i = 1;
        int c = 0;

        while (sc.hasNextLine()) {
            String s = sc.nextLine();
            if (s.length() == 0) {
                continue;
            }
            s = s.strip();

            String[] arr5 = s.split(" ");
            if (!function2(arr5[0]) && arr5[0].charAt((arr5[0].length()) - 1) == ':') {

                String[] arr2 = new String[arr5.length - 1];
                for (int k = 0; k < arr5.length - 1; k++) {
                    arr2[k] = arr5[k + 1];
                }
                dict.put(arr5[0].substring(0, arr5[0].length() - 1), c);
                arr5 = arr2;

            }
            c++;
            helper2.add(arr5);

        }

        for (int l = 0; l < helper2.size(); l++) {
            String res = "";

            String[] arr = helper2.get(l);

            if (arr.length == 1 && !arr[0].equals("hlt")) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }

            if (arr.length > 5) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }

            // System.out.println(dict);

            if (l == helper2.size() - 1 && !arr[0].equals("hlt")) {
                System.out.println("Missing hlt instruction");
                System.exit(0);
            }

            if (arr[0].equals("hlt") && l != helper2.size() - 1) {
                System.out.println("hlt not being used as the last instruction");
                System.exit(0);
            }

            res = function(arr[0], arr, i);
            if (!res.equals("")) {
                bin.add(res);
            }
            i++;
        }

        for (int j = 0; j < bin.size(); j++) {
            if (bin.get(j).length() == 16) {
                System.out.println(bin.get(j));
            }
        }
        //
    }

    public static boolean function2(String a) {

        if (a.equals("var")) {
            return true;
        } else if (a.equals("add")) {
            return true;
        } else if (a.equals("sub")) {
            return true;
        } else if (a.equals("mov")) {
            return true;
        } else if (a.equals("ld")) {
            return true;
        } else if (a.equals("st")) {
            return true;
        } else if (a.equals("mul")) {
            return true;
        } else if (a.equals("div")) {
            return true;
        } else if (a.equals("rs")) {
            return true;
        } else if (a.equals("ls")) {
            return true;
        } else if (a.equals("xor")) {
            return true;
        } else if (a.equals("or")) {
            return true;
        } else if (a.equals("and")) {
            return true;
        } else if (a.equals("not")) {
            return true;
        } else if (a.equals("cmp")) {
            return true;
        } else if (a.equals("jmp")) {
            return true;
        } else if (a.equals("jlt")) {
            return true;
        } else if (a.equals("jgt")) {
            return true;
        } else if (a.equals("je")) {
            return true;
        } else if (a.equals("hlt")) {
            return true;
        } else {
            return false;
        }
    }

    public static String reg(String r) {

        if (r.equals("reg0") || r.equals("r0") || r.equals("Reg0") || r.equals("R0")) {
            return "000";
        }
        if (r.equals("reg1") || r.equals("r1") || r.equals("Reg1") || r.equals("R1")) {
            return "001";
        }
        if (r.equals("reg2") || r.equals("r2") || r.equals("Reg2") || r.equals("R2")) {
            return "010";
        }
        if (r.equals("reg3") || r.equals("r3") || r.equals("Reg3") || r.equals("R3")) {
            return "011";
        }
        if (r.equals("reg4") || r.equals("r4") || r.equals("Reg4") || r.equals("R4")) {
            return "100";
        }
        if (r.equals("reg5") || r.equals("r5") || r.equals("Reg5") || r.equals("R5")) {
            return "101";
        }
        if (r.equals("reg6") || r.equals("r6") || r.equals("Reg6") || r.equals("R6")) {
            return "110";
        }
        if (r.equals("FLAGS")) {
            return "111";
        } else {
            return "Typos in instruction name or Register";
        }
    }

    public static String function(String a, String[] arr, int count) {
        String A = "00000";
        String B = "00001";
        String C = "00010";
        String D = "00011";
        String E = "00100";
        String F = "00101";
        String G = "00110";
        String H = "00111";
        String H1 = "01000";
        String I = "01001";
        String J = "01010";
        String K = "01011";
        String L = "01100";
        String M = "01101";
        String N = "01110";
        String O = "01111";
        String P = "10000";
        String Q = "10001";
        String R = "10010";
        String S = "10011";

        String s = "";

        if (arr.length == 1 && !arr[0].equals("hlt")) {
            System.out.println("Typos in instruction name or Register");
            return "";
        } else if (a.equals("var")) {

            if (bin.size() != 0) {
                System.out.println("Variables not declared at the beginning");
                System.exit(0);
            }
            if (arr.length == 2) {
                help.add(arr[1]);
                return "";
            }

            else {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
                return "";
            }
        } else if (a.equals("add")) {
            s += A;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;

        } else if (a.equals("sub")) {
            s += B;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;
        } else if (a.equals("mov")) {

            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[2].charAt(0) == '$') {
                s += C;
                s += reg(arr[1]);
                int m = Integer.parseInt(arr[2].substring(1));
                if (m >= 0 && m <= 255) {
                    String r = Integer.toBinaryString(m);
                    s += intstantvariable(r);
                } else {
                    System.out.println("Illegal Immediate values (less than 0 or more than 255)");
                    System.exit(0);
                }
            } else if (arr[1].charAt(0) == 'r' || arr[1].charAt(0) == 'R' || arr[1].equals("FLAGS")) {
                s += D;
                s += "00000";
                s += reg(arr[1]);
                s += reg(arr[2]);
            } else {
                System.out.println("Typos in instruction name or Register");
                System.exit(0);
            }
            return s;
        }

        else if (a.equals("ld")) {
            s += E;
            s += reg(arr[1]);
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[1] == "FLAGS" || arr[2].equals("FLAGS")) {
                System.out.println("Illegal use of FLAGS register");
                System.exit(0);
            }
            if (dict.get(arr[2]) != null) {
                System.out.println("Misuse of labels as variables");
                System.exit(0);
            } else if (help.contains(arr[2])) {
                String m = Integer.toBinaryString(count);
                s += intstantvariable(m);
            }

            else {
                System.out.println("Use of undefined variables");
                System.exit(0);

            }
            return s;
        } else if (a.equals("st")) {
            s += F;
            s += reg(arr[1]);
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[1] == "FLAGS" || arr[2].equals("FLAGS")) {
                System.out.println("Illegal use of FLAGS register");
                System.exit(0);
            }
            if (dict.get(arr[2]) != null) {
                System.out.println("Misuse of labels as variables");
                System.exit(0);
            } else if (help.contains(arr[2])) {
                String m = Integer.toBinaryString(count);
                s += intstantvariable(m);
            } else {
                System.out.println("Use of undefined variables");
                System.exit(0);
            }
            return s;
        } else if (a.equals("mul")) {
            s += G;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {

                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;
        } else if (a.equals("div")) {
            s += H;
            s += "00000";
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 3 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;
        } else if (a.equals("rs")) {
            s += H1;
            s += reg(arr[1]);
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[2].charAt(0) == '$') {
                int m = Integer.parseInt(arr[2].substring(1));
                if (m >= 0 && m <= 255) {
                    String r = Integer.toBinaryString(m);
                    s += intstantvariable(r);
                } else {
                    System.out.println("Illegal Immediate values (less than 0 or more than 255)");
                    System.exit(0);
                }
            } else {
                return "Typos in instruction name or Register";
            }
            return s;
        } else if (a.equals("ls")) {
            s += I;
            s += reg(arr[1]);
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[2].charAt(0) == '$') {
                int m = Integer.parseInt(arr[2].substring(1));
                if (m >= 0 && m <= 255) {
                    String r = Integer.toBinaryString(m);
                    s += intstantvariable(r);
                } else {

                    System.out.println("Illegal Immediate values (less than 0 or more than 255)");
                    System.exit(0);
                }
            } else if (arr[2].substring(0, 3) == "reg") {
                s += reg(arr[2]);
            } else {
                return "Typos in instruction name or Register";
            }
            return s;
        } else if (a.equals("xor")) {
            s += J;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;

        } else if (a.equals("or")) {
            s += K;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;
        }

        else if (a.equals("and")) {
            s += L;
            s += "00";
            if (arr.length != 4) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;

        }

        else if (a.equals("not")) {
            s += M;
            s += "00000";
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                if (arr[i].equals("FLAGS")) {
                    System.out.println("Illegal use of FLAGS register");
                    System.exit(0);
                }
                if (arr.length == 4 && (arr[i].charAt(0) == 'R' || arr[i].charAt(0) == 'r')) {
                    s = s + reg(arr[i]);
                } else {
                    System.out.println("Typos in instruction name or Register");
                    System.exit(0);
                }
            }
            return s;
        }

        else if (a.equals("cmp")) {
            s += N;
            s += "00000";
            if (arr.length != 3) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            if (arr[1] == "FLAGS" || arr[2].equals("FLAGS")) {
                System.out.println("Illegal use of FLAGS register");
                System.exit(0);
            }
            for (int i = 1; i < arr.length; i++) {
                s += reg(arr[i]);
            }
            return s;
        } else if (a.equals("jmp")) {
            s += O;
            s += "000";
            String m = jumphelp(arr, count);
            s += intstantvariable(m);

            return s;
        } else if (a.equals("jlt")) {
            s += P;
            s += "000";
            String m = jumphelp(arr, count);
            s += intstantvariable(m);

            return s;
        } else if (a.equals("jgt")) {
            s += Q;
            s += "000";
            String m = jumphelp(arr, count);
            s += intstantvariable(m);

            return s;
        } else if (a.equals("je")) {
            s += R;
            s += "000";

            String m = jumphelp(arr, count);
            s += intstantvariable(m);

            return s;
        } else if (a.equals("hlt")) {
            s += S;
            if (arr.length != 1) {
                System.out.println("Wrong syntax used for instructions");
                System.exit(0);
            }
            s += "00000000000";
            return s;
        }

        else {
            System.out.println("Typos in instruction name or Register");
            System.exit(0);
            return " ";
        }
    }

    public static String jumphelp(String[] arr, int count) {
        if (arr.length != 2) {
            System.out.println("Wrong syntax used for instructions");
            System.exit(0);
        }
        if (arr[1] == "FLAGS") {
            System.out.println("Illegal use of FLAGS register");
            System.exit(0);
        }
        if (help.contains(arr[1])) {
            System.out.println("Misuse of variable as label");
            System.exit(0);
        }
        if (dict.get(arr[1]) == null) {
            System.out.println("Use of undefined labels");
            System.exit(0);
        }
        // int r=dict.get(arr[1])-1;
        String m = Integer.toBinaryString(count - 1);
        return m;
    }

    public static String intstantvariable(String a) {
        int c = a.length();
        int x = 8 - c;
        String s = "";
        for (int i = 0; i < x; i++) {
            s = s + "0";
        }
        s = s + a;
        return s;
    }
}