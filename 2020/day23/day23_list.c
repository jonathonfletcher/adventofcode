#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


#define NDROP   (3)
#define SMOL_ITERATIONS    (100)
#define HUGE_SIZE    (1000000)
#define HUGE_ITERATIONS (10000000)



struct e {
    int i;
    int v;
    struct e *next;
};



void print_input_list(struct e *input, struct e *offset)
{
struct e *n = input;

    while (1)
    {
        if (n == offset) {
            printf("(%d)", n->v);
        } else {
            printf("%s%d%s", n==input?"":" ", n->v, n->next==input?"":" ");
        }

        n = n->next;
        if (n == input) {
            break;
        }
    }
    printf("\n");
}



inline struct e *find_list(register int val, struct e *head)
{
register struct e *n = head;

    do
    {
        if (n->v == val) {
            return n;
        }
        n = n->next;
    } while (n != head);
    return n;
}



struct e *find_final_list(struct e *head, struct e *offset_ptr, int offset)
{
int i = offset;
struct e *tmp = head;

    while (i-- > 0)
    {
        tmp = tmp->next;
    }

    while (tmp != offset_ptr)
    {
        tmp = tmp->next;
        head = head->next;
    }

    return head;
}



int find_dc_list(register int val, register struct e *drop_list, int minval, int maxval)
{
    while (1)
    {
        val -= 1;
        if (val < minval) {
            val = maxval;
        }
        if (val != drop_list->v && val != drop_list->next->v && val != drop_list->next->next->v) {
            return val;
        }
    }
}



void print_final_label_list(struct e *head)
{
struct e *one_ptr = find_list(1, head);
struct e *n = one_ptr->next;

    while (n != one_ptr) {
        printf("%d", n->v);
        n = n->next;
    }
    printf("\n");
}



long long final_product_list(struct e *head)
{
struct e *one_ptr = find_list(1, head);

    printf("%ld * %ld\n", (long)one_ptr->next->v, (long)one_ptr->next->next->v);
    return (long)one_ptr->next->v * (long)one_ptr->next->next->v;
}



void update_circle_list(struct e *head, struct e *offset, int input_length, int minval, int maxval)
{

    struct e *drop_list = offset->next;
    int dc = find_dc_list(offset->v, drop_list, minval, maxval);
    struct e *dc_list = find_list(dc, drop_list->next->next->next);
    offset->next = drop_list->next->next->next;
    drop_list->next->next->next = dc_list->next;
    dc_list->next = drop_list;
}



struct e *make_input_list(const char *input_str, const int input_length)
{
struct e *input_list = NULL;
struct e *head = NULL;
struct e *tail = NULL;
int maxval = -1;

    input_list = calloc(input_length, sizeof(struct e));
    for ( int i=0 ; i < strlen(input_str) ; i++ )
    {
        if (i == 0) {
            head = &input_list[i];
            tail = head;
            head->i = i;
            head->next = tail;
        } else {
            struct e *n = &input_list[i];
            n->i = i;
            if (head == tail) {
                head->next = n;
            }
            tail->next = n;
            tail = n;
            tail->next = head;
        }
        tail->v = input_str[i] - 48;
        if (tail->v > maxval) {
            maxval = tail->v;
        }
    }
    for ( int i = strlen(input_str) ; i < input_length ; i++ )
    {
        struct e *n = &input_list[i];
        maxval = maxval+1;
        n->i = i;
        n->v = maxval;
        if (head == tail) {
            head->next = n;
        }
        tail->next = n;
        tail = n;
        tail->next = head;
    }

    return head;
}



void run(const char *input_str, int huge)
{
const int input_length = huge ? HUGE_SIZE : strlen(input_str);
struct e *input_list = make_input_list(input_str, input_length);
struct e *offset_ptr = input_list;
struct e *final_list = input_list;
int offset = 0;
int minval, maxval;
int iterations = huge ? HUGE_ITERATIONS : SMOL_ITERATIONS;
time_t start_time, current_time;

    minval = 1;
    maxval = input_length;

    // printf("%d (%d, %d)\n", input_length, minval, maxval);

    start_time = time(NULL);
    for ( register int j=0 ; j < iterations ; j++ )
    {
        if (huge && j > 0 && j % 5000 == 0 ) {
            current_time = time(NULL);
            printf("%d / %d (%.0f%%)\n", j, iterations, 100.*j/iterations);
            printf("%lds elapsed / %.0lfs remaining\n",
                (long)current_time-start_time,
                (double)((current_time-start_time)/(1.*j/iterations)-(current_time-start_time)));
        }

        update_circle_list(input_list, offset_ptr, input_length, minval, maxval);

        offset_ptr = offset_ptr->next;
    }

    offset = iterations % input_length;
    final_list = find_final_list(input_list, offset_ptr, offset);

    if (huge) {
        current_time = time(NULL);
        printf("%lds total\n", (long)current_time-start_time);
        printf("%lld\n", final_product_list(final_list));
    } else {
        print_input_list(final_list, offset_ptr);
        print_final_label_list(final_list);
    }

    free(input_list);
}


int main(int argc, char **argv)
{
const char *input_str = "389125467";

    run(input_str, 0);
    run(input_str, 1);

    return EXIT_SUCCESS;
}


