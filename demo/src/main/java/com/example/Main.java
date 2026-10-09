package com.example;

import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
/* 
        //java.lang.NullPointerException
        String name=null;
        System.out.println(name.length());


        //java.lang.IndexOutOfBoundsException
        LinkedList<String> list = new LinkedList<>();
        list.add("Hello");
        System.out.println(list.get(0));
        System.out.println(list.get(1));

        //ArithmeticException
        int a=10;
        int b=0;
        System.out.println(a/b);

        //ClassCastException
        Object obj = "abc";
        Integer num1 =  (Integer) obj;
        System.out.println(num1);

        //NumberFormatException
        String str = "abc";
        Integer num2 =  Integer.parseInt(str);
        System.out.println(num2);

        //StackOverflowError
        methodePrivate();
*/
        //ConcurrentModificationException
        LinkedList<Integer> list = new LinkedList<>();
        list.add(1);
        list.add(2);
        for (Integer s : list) {
            list.add(3);            
        }

    }

    private static void methodePrivate() {
        methodePrivate();
    }
}