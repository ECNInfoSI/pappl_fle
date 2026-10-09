package com.example;

import java.util.LinkedList;

/**
 * Classe principale du programme de démonstration.
 * Elle illustre différents types d'exceptions Java et
 * permet de tester la saisie d'un personnage via la console.
 *
 * @author Maxence SCHWERER et Corentin GODARD
 */
public class Main {

    /**
     * Point d'entrée du programme.
     * Cette méthode crée un personnage et lance la saisie de son âge
     * depuis l'entrée standard.
     *
     * @param args arguments passés en ligne de c   ommande
     */
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
        //LinkedList<Integer> list = new LinkedList<>();
        //list.add(1);
        //list.add(2);
        //for (Integer s : list) {
        //    list.add(3);            
        //}

        Personnage Maxence = new Personnage();
        Maxence.demander_throws();
    }

}

