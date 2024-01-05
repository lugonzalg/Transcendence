#!/bin/bash

# VARIABLES
all_services=false
clean=false
build=false
restart=false
clean_name=""
build_name=""

if [ "$#" -eq 0 ]; then
    echo "Error: no parameters given"
    exit 1
fi

handle_response () {

    echo "Handle response"
    case $choice in
    [Yy])
        echo "Choice is yes"
        ;;
    [Nn])
        echo "Choice is not"
        ;;
    *)
        echo "Not valid choice!"
        return 0
        ;;
    esac

    return 1
}

create_service_dependencies () {
    mkdir -p ./volumes/$1/log
    mkdir -p ./volumes/$1/data
}

delete_service () {
    echo "Deleteing service $1 dependencies!" 
    rm -rf ./volumes/$1
}

clean_service () {

    echo "Service: $1"
    case $1 in
        login)
            delete_service backend/$1
            create_service_dependencies backend/$1
            ;;
        postgres)
            delete_service database/$1
            create_service_dependencies database/$1
            ;;
        *)
            echo "unknown service!"
            ;;
    esac
}

Clean () {

    if $all_services; then
        echo -n "Do you want to clean all services? [Yy/Nn]: "
        read choice

        handle_response $choice
        retval=$?

        if [ $retval  -eq 1 ]; then
            echo -n "Do you still want to clean all services? [Yy/Nn]: "
            read choice

            handle_response $choice
            retval=$?

            if [ $retval  -eq 1 ]; then
                rm -rf ./transcendence/volumes
                bash ./base.sh
            fi
        fi
    else

        echo -n "What is the service name that you want to delete? [login/postgres]: "
        read choice_name

        clean_service $choice_name
    fi

}

Build () {

    if $all_services; then
        echo -n "Do you want to build all services? [Yy/Nn]: "
        read choice

        handle_response $choice
        retval=$?

        if [ $retval  -eq 1 ]; then
            make build-all
        fi

    else

        echo -n "What is the service you want to build? [login/postgres]: "
        read choice_name

        make build SERVICE=$choice_name
    fi
}

Restart () {

    if $all_services; then
        echo -n "Do you want to restart all services? [Yy/Nn]: "
        read choice

        handle_response $choice
        retval=$?

        if [ $retval  -eq 1 ]; then
            make restart-all
        fi

    else

        echo -n "What is the service you want to restart? [login/postgres]: "
        read choice_name

        make restart SERVICE=$choice_name
    fi
}

while [ "$#" -gt 0 ]; do
    case $1 in
    --clean)
        clean=true
        ;;
    --build)
        build=true
        ;;
    --restart)
        restart=true
        ;;
    --all)
        all_services=true
        ;;
    *)
        echo "Unknown command: $1"
        ;;
    esac
    shift
done

if $clean; then
    Clean
fi

if $build; then
    Build
fi

if $restart; then
    Restart
fi