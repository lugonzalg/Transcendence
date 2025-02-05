#!/bin/bash

# VARIABLES
all_services=false
clean=false
build=false
restart=false
stop=false
raise=false
migrate=false
follow=false
clean_name=""
build_name=""

backend_opts=login
database_opts=postgre
frontend_opts=vue
general_opts="$backend_opts/$frontend_opts/$database_opts"

services_path="./transcendence/volumes"

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

    service_path=$services_path/$volume/$service

    echo $service_path
    mkdir -p $service_path
    mkdir -p $service_path/data
    mkdir -p $service_path/log
}

delete_service () {

    echo "Deleteing service $1 dependencies!" 

    rm -rf $services_path/$volume/$service
}

clean_service () {

    echo "Service: $service"
    delete_service $volume $service
    create_service_dependencies $volume $service
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

        echo -n "What is the service name that you want to delete? [$general_opts]: "
        read service

        case $service in

        login)
            volume="backend"
            ;;
        postgres)
            volume="database"
            ;;
        *)
            echo "Service: $service does not exists"
            volume=""
            ;;

        esac
        if [ $volume ]; then
            clean_service $volume $service
        fi
    fi

}

Command () {

    mode=$1

    if $all_services; then
        echo -n "Do you want to $mode all services? [Yy/Nn]: "
        read choice

        handle_response $choice
        retval=$?

        if [ $retval  -eq 1 ]; then
            make $mode-all
        fi

    else

        echo -n "What is the service you want to $mode? [$general_opts]: "
        read service

        make $mode SERVICE=$service
    fi
}

if [ "$#" -eq 0 ]; then
    echo "manager: try --help for more information"
    exit 1
fi

help () {
    echo "-B, --build build service image" 
    echo "-C, --clean delete service dependencies" 
    echo "-F, --follow follow the container image logs" 
    echo "-H, --help information about the commands" 
    echo "-M, --migrate migrate the django service data models" 
    echo "-RA, --raise start the service container" 
    echo "-RE, --restart restart the service container" 
    echo "-S, --stop stop the service container" 
}

while [ "$#" -gt 0 ]; do
    case $1 in
    --build|-B)
        build=true
        ;;
    --clean|-C)
        clean=true
        ;;
    --help|-H)
        help
        exit 0
        ;;
    --migrate|-M)
        migrate=true
        ;;
    --raise|-RA)
        raise=true
        ;;
    --restart|-RE)
        restart=true
        ;;
    --stop|-S)
        stop=true
        ;;
    --all|-A)
        all_services=true
        ;;
    #help
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
    Command build
fi

if $restart; then
    Command restart
fi

if $stop; then
    Command stop
fi

if $raise; then
    Command raise
fi

if $migrate; then
    Command migrate
fi

if $migrate; then
    Command follow
fi