package demo

import (
	"database/sql"
	"errors"
	"fmt"
	"sort"
	"strings"
	"time"

	"github.com/ebisol/api/app/logger"
	_ "github.com/lib/pq"
)

var db *sql.DB

func init() {
	var err error
	db, err = sql.Open("postgres", "host=localhost port=5433 user=ciao password=Kir0#alpha dbname=postgres sslmode=disable")
	if err != nil {
		logger.StackLogger(err)
		panic(err)
	}
}

// GetDB
func (a *TableCreateDemo) GetDB() *sql.DB {
	return db
}

// TableCreateDemo is the model for table table_create_demo
type TableCreateDemo struct {
	ID                int        `json:"id"`
	IntDemo           int        `json:"int_demo"`
	TextDemo          string     `json:"text_demo"`
	BoolDemo          bool       `json:"bool_demo"`
	FloatDemo         float64    `json:"float_demo"`
	TimestampDemo     time.Time  `json:"timestamp_demo"`
	IntDemoNull       *int       `json:"int_demo_null"`
	TextDemoNull      *string    `json:"text_demo_null"`
	BoolDemoNull      *bool      `json:"bool_demo_null"`
	FloatDemoNull     *float64   `json:"float_demo_null"`
	TimestampDemoNull *time.Time `json:"timestamp_demo_null"`
}

// TableCreateDemoCollection ...
type TableCreateDemoCollection []*TableCreateDemo

// SelectXCore is a auto generate method for select data from TableCreateDemo table
func (a *TableCreateDemo) SelectXCore(tx *sql.Tx, query string, args ...interface{}) ([]*TableCreateDemo, error) {
	var insArr []*TableCreateDemo
	var rows *sql.Rows
	var err error
	if (args != nil) && (!(len(args) == 1 && args[0] == nil)) {
		if tx != nil {
			rows, err = tx.Query(query, args...)
		} else {
			rows, err = db.Query(query, args...)
		}
		if err != nil {
			logger.StackLogger(err)
			return nil, err
		}
	} else {
		if tx != nil {
			rows, err = tx.Query(query)
		} else {
			rows, err = db.Query(query)
		}
		if err != nil {
			logger.StackLogger(err)
			return nil, err
		}
	}
	if rows != nil {
		defer rows.Close()
		for rows.Next() {
			item := TableCreateDemo{}
			err := rows.Scan(&item.ID, &item.IntDemo, &item.TextDemo, &item.BoolDemo, &item.FloatDemo, &item.TimestampDemo, &item.IntDemoNull, &item.TextDemoNull, &item.BoolDemoNull, &item.FloatDemoNull, &item.TimestampDemoNull)
			if err != nil {
				logger.StackLogger(err)
				return nil, err
			}
			insArr = append(insArr, &item)
		}
		err = rows.Err()
		if err != nil {
			logger.StackLogger(err)
			return nil, err
		}
	}
	return insArr, nil
}

// InsertCore ...
func (a *TableCreateDemo) InsertCore(tx *sql.Tx, item TableCreateDemo) (int, error) {
	var lastInsertID int
	var err error
	query := `INSERT INTO table_create_demo (
		int_demo,
		text_demo,
		bool_demo,
		float_demo,
		timestamp_demo,
		int_demo_null,
		text_demo_null,
		bool_demo_null,
		float_demo_null,
		timestamp_demo_null)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) returning id;`
	if tx != nil {
		err = tx.QueryRow(query, item.IntDemo, item.TextDemo, item.BoolDemo, item.FloatDemo, item.TimestampDemo, item.IntDemoNull, item.TextDemoNull, item.BoolDemoNull, item.FloatDemoNull, item.TimestampDemoNull).Scan(&lastInsertID)
	} else {
		err = db.QueryRow(query, item.IntDemo, item.TextDemo, item.BoolDemo, item.FloatDemo, item.TimestampDemo, item.IntDemoNull, item.TextDemoNull, item.BoolDemoNull, item.FloatDemoNull, item.TimestampDemoNull).Scan(&lastInsertID)
	}
	if err != nil {
		logger.StackLogger(err)
		return 0, err
	}
	return lastInsertID, nil
}

// UpdateCore ...
func (a *TableCreateDemo) UpdateCore(tx *sql.Tx, i int, item TableCreateDemo) error {
	query := `
	UPDATE table_create_demo
	SET int_demo = $2,
		text_demo = $3,
		bool_demo = $4,
		float_demo = $5,
		timestamp_demo = $6,
		int_demo_null = $7,
		text_demo_null = $8,
		bool_demo_null = $9,
		float_demo_null = $10,
		timestamp_demo_null = $11
	WHERE id = $1`
	var res sql.Result
	var err error
	if tx != nil {
		res, err = tx.Exec(query, i, item.IntDemo, item.TextDemo, item.BoolDemo, item.FloatDemo, item.TimestampDemo, item.IntDemoNull, item.TextDemoNull, item.BoolDemoNull, item.FloatDemoNull, item.TimestampDemoNull)
	} else {
		res, err = db.Exec(query, i, item.IntDemo, item.TextDemo, item.BoolDemo, item.FloatDemo, item.TimestampDemo, item.IntDemoNull, item.TextDemoNull, item.BoolDemoNull, item.FloatDemoNull, item.TimestampDemoNull)
	}
	if err != nil {
		logger.StackLogger(err)
		return err
	}
	return a.RowChangeCheck(i, res)
}

// DeleteCore ...
func (a *TableCreateDemo) DeleteCore(tx *sql.Tx, i int) error {
	query := `
		DELETE FROM table_create_demo
		WHERE id = $1`
	var res sql.Result
	var err error
	if tx != nil {
		res, err = tx.Exec(query, i)
	} else {
		res, err = db.Exec(query, i)
	}
	if err != nil {
		logger.StackLogger(err)
		return err
	}
	return a.RowChangeCheck(i, res)
}

// SelectX is a auto generate method for select data from TableCreateDemo table
func (a *TableCreateDemo) SelectX(query string) ([]*TableCreateDemo, error) {
	return a.SelectXCore(nil, query, nil)
}

// SelectXwithArgs is a auto generate method for select data from TableCreateDemo table
func (a *TableCreateDemo) SelectXwithArgs(query string, args ...interface{}) ([]*TableCreateDemo, error) {
	return a.SelectXCore(nil, query, args...)
}

// SelectXwithTransc is a auto generate method for select data from TableCreateDemo table
func (a *TableCreateDemo) SelectXwithTransc(tx *sql.Tx, query string) ([]*TableCreateDemo, error) {
	return a.SelectXCore(tx, query, nil)
}

// SelectXwithTranscwithArgs is a auto generate method for select data from TableCreateDemo table
func (a *TableCreateDemo) SelectXwithTranscwithArgs(tx *sql.Tx, query string, args ...interface{}) ([]*TableCreateDemo, error) {
	return a.SelectXCore(tx, query, args...)
}

// CountX is a auto generate method for count data in TableCreateDemo table
func (a *TableCreateDemo) CountX(query string) (int, error) {
	count := 0
	err := db.QueryRow(query).Scan(&count)
	if err != nil {
		logger.StackLogger(err)
		return 0, err
	}
	return count, nil
}

// Insert ...
func (a *TableCreateDemo) Insert(item TableCreateDemo) (int, error) {
	return a.InsertCore(nil, item)
}

// InsertwithTransc ...
func (a *TableCreateDemo) InsertwithTransc(tx *sql.Tx, item TableCreateDemo) (int, error) {
	return a.InsertCore(tx, item)
}

// Update ...
func (a *TableCreateDemo) Update(i int, item TableCreateDemo) error {
	return a.UpdateCore(nil, i, item)
}

// UpdatewithTransc ...
func (a *TableCreateDemo) UpdatewithTransc(tx *sql.Tx, i int, item TableCreateDemo) error {
	return a.UpdateCore(tx, i, item)
}

// Delete ...
func (a *TableCreateDemo) Delete(i int) error {
	return a.DeleteCore(nil, i)
}

// DeletewithTransc ...
func (a *TableCreateDemo) DeletewithTransc(tx *sql.Tx, i int) error {
	return a.DeleteCore(tx, i)
}

// RowChangeCheck is for update and delete, check the affected rows been affected
func (a *TableCreateDemo) RowChangeCheck(i int, res sql.Result) error {
	if res != nil {
		affect, err := res.RowsAffected()
		if err != nil {
			logger.StackLogger(err)
			return err
		}
		switch affect {
		case 0:
			return fmt.Errorf("%v rows changed, id = %v does not exist", affect, i)
		case 1:
			return nil
		default:
			return fmt.Errorf("%v rows changed", affect)
		}
	} else {
		return fmt.Errorf("res is nil, id = %v", i)
	}
}

// Wrapper ...
func (a *TableCreateDemo) Wrapper(item TableCreateDemo) (newitem TableCreateDemo) {
	newitem.ID = item.ID
	newitem.IntDemo = item.IntDemo
	newitem.TextDemo = item.TextDemo
	newitem.BoolDemo = item.BoolDemo
	newitem.FloatDemo = item.FloatDemo
	newitem.TimestampDemo = item.TimestampDemo
	newitem.IntDemoNull = item.IntDemoNull
	newitem.TextDemoNull = item.TextDemoNull
	newitem.BoolDemoNull = item.BoolDemoNull
	newitem.FloatDemoNull = item.FloatDemoNull
	newitem.TimestampDemoNull = item.TimestampDemoNull
	return newitem
}

func typeCompareFunc(p1, p2 interface{}, orderstr string) bool {
	if orderstr == "desc" {
		switch p1.(type) {
		case bool:
			if p1.(bool) == true && p2.(bool) == false {
				return true
			}
			return false
		case int:
			return p1.(int) > p2.(int)
		case int64:
			return p1.(int64) > p2.(int64)
		case float32:
			return p1.(float32) > p2.(float32)
		case float64:
			return p1.(float64) > p2.(float64)
		case string:
			return p1.(string) > p1.(string)
		case time.Time:
			return (p1.(time.Time)).After(p2.(time.Time))
		case *bool:
			if p1 != (*bool)(nil) && p2 != (*bool)(nil) {
				if *p1.(*bool) == true && *p2.(*bool) == false {
					return true
				}
			} else if p1 != (*bool)(nil) && p2 == (*bool)(nil) {
				return true
			}
			return false
		case *int:
			if p1 != (*int)(nil) && p2 != (*int)(nil) {
				return *p1.(*int) > *p2.(*int)
			} else if p1 != (*int)(nil) && p2 == (*int)(nil) {
				return true
			}
			return false
		case *int64:
			if p1 != (*int64)(nil) && p2 != (*int64)(nil) {
				return *p1.(*int64) > *p2.(*int64)
			} else if p1 != (*int64)(nil) && p2 == (*int64)(nil) {
				return true
			}
			return false
		case *float32:
			if p1 != (*float32)(nil) && p2 != (*float32)(nil) {
				return *p1.(*float32) > *p2.(*float32)
			} else if p1 != (*float32)(nil) && p2 == (*float32)(nil) {
				return true
			}
			return false
		case *float64:
			if p1 != (*float64)(nil) && p2 != (*float64)(nil) {
				return *p1.(*float64) > *p2.(*float64)
			} else if p1 != (*float64)(nil) && p2 == (*float64)(nil) {
				return true
			}
			return false
		case *string:
			if p1 != (*string)(nil) && p2 != (*string)(nil) {
				return *p1.(*string) > *p2.(*string)
			} else if p1 != (*string)(nil) && p2 == (*string)(nil) {
				return true
			}
			return false
		case *time.Time:
			if p1 != (*time.Time)(nil) && p2 != (*time.Time)(nil) {
				return (*p1.(*time.Time)).After(*p2.(*time.Time))
			} else if p1 != (*time.Time)(nil) && p2 == (*time.Time)(nil) {
				return true
			}
			return false
		default:
			return false
		}
	} else {
		switch p1.(type) {
		case bool:
			if p1.(bool) == true && p2.(bool) == false {
				return false
			}
			return true
		case int:
			return p1.(int) < p2.(int)
		case int64:
			return p1.(int64) < p2.(int64)
		case float32:
			return p1.(float32) < p2.(float32)
		case float64:
			return p1.(float64) < p2.(float64)
		case string:
			return p1.(string) < p1.(string)
		case time.Time:
			return (p1.(time.Time)).Before(p2.(time.Time))
		case *bool:
			if p1 != (*bool)(nil) && p2 != (*bool)(nil) {
				if *p1.(*bool) == false && *p2.(*bool) == true {
					return true
				}
			} else if p1 != (*bool)(nil) && p2 == (*bool)(nil) {
				return true
			}
			return false
		case *int:
			if p1 != (*int)(nil) && p2 != (*int)(nil) {
				return *p1.(*int) < *p2.(*int)
			} else if p1 != (*int)(nil) && p2 == (*int)(nil) {
				return true
			}
			return false
		case *int64:
			if p1 != (*int64)(nil) && p2 != (*int64)(nil) {
				return *p1.(*int64) < *p2.(*int64)
			} else if p1 != (*int64)(nil) && p2 == (*int64)(nil) {
				return true
			}
			return false
		case *float32:
			if p1 != (*float32)(nil) && p2 != (*float32)(nil) {
				return *p1.(*float32) < *p2.(*float32)
			} else if p1 != (*float32)(nil) && p2 == (*float32)(nil) {
				return true
			}
			return false
		case *float64:
			if p1 != (*float64)(nil) && p2 != (*float64)(nil) {
				return *p1.(*float64) < *p2.(*float64)
			} else if p1 != (*float64)(nil) && p2 == (*float64)(nil) {
				return true
			}
			return false
		case *string:
			if p1 != (*string)(nil) && p2 != (*string)(nil) {
				return *p1.(*string) < *p2.(*string)
			} else if p1 != (*string)(nil) && p2 == (*string)(nil) {
				return true
			}
			return false
		case *time.Time:
			if p1 != (*time.Time)(nil) && p2 != (*time.Time)(nil) {
				return (*p1.(*time.Time)).Before(*p2.(*time.Time))
			} else if p1 != (*time.Time)(nil) && p2 == (*time.Time)(nil) {
				return true
			}
			return false
		default:
			return false
		}
	}
}

// SortBy ...
func (c TableCreateDemoCollection) SortBy(columnName string, orderstr string) error {
	if orderstr != "asc" && orderstr != "desc" {
		return fmt.Errorf("not supported order keyword: %v", orderstr)
	}
	comparedFunc := func(p1, p2 *TableCreateDemo) bool {
		if columnName == "int_demo" {
			return typeCompareFunc(p1.IntDemo, p2.IntDemo, orderstr)
		} else if columnName == "text_demo" {
			return typeCompareFunc(p1.TextDemo, p2.TextDemo, orderstr)
		} else if columnName == "bool_demo" {
			return typeCompareFunc(p1.BoolDemo, p2.BoolDemo, orderstr)
		} else if columnName == "float_demo" {
			return typeCompareFunc(p1.FloatDemo, p2.FloatDemo, orderstr)
		} else if columnName == "timestamp_demo" {
			return typeCompareFunc(p1.TimestampDemo, p2.TimestampDemo, orderstr)
		} else if columnName == "int_demo_null" {
			return typeCompareFunc(p1.IntDemoNull, p2.IntDemoNull, orderstr)
		} else if columnName == "text_demo_null" {
			return typeCompareFunc(p1.TextDemoNull, p2.TextDemoNull, orderstr)
		} else if columnName == "bool_demo_null" {
			return typeCompareFunc(p1.BoolDemoNull, p2.BoolDemoNull, orderstr)
		} else if columnName == "float_demo_null" {
			return typeCompareFunc(p1.FloatDemoNull, p2.FloatDemoNull, orderstr)
		} else if columnName == "timestamp_demo_null" {
			return typeCompareFunc(p1.TimestampDemoNull, p2.TimestampDemoNull, orderstr)
		}
		return typeCompareFunc(p1.ID, p2.ID, orderstr)
	}
	TableCreateDemoBy(comparedFunc).Sort(c)
	return nil
}

// TableCreateDemoBy is the type of a "less" function that defines the ordering of its Planet arguments.
type TableCreateDemoBy func(p1, p2 *TableCreateDemo) bool

// Sort is a method on the function type, By, that sorts the argument slice according to the function.
func (by TableCreateDemoBy) Sort(tableCreateDemos []*TableCreateDemo) {
	ps := &tableCreateDemoSorter{
		tableCreateDemos: tableCreateDemos,
		by:               by, // The Sort method's receiver is the function (closure) that defines the sort order.
	}
	sort.Sort(ps)
}

// tableCreateDemoSorter joins a By function and a slice of Planets to be sorted.
type tableCreateDemoSorter struct {
	tableCreateDemos []*TableCreateDemo
	by               func(p1, p2 *TableCreateDemo) bool // Closure used in the Less method.
}

// Len is part of sort.Interface.
func (s *tableCreateDemoSorter) Len() int {
	return len(s.tableCreateDemos)
}

// Swap is part of sort.Interface.
func (s *tableCreateDemoSorter) Swap(i, j int) {
	s.tableCreateDemos[i], s.tableCreateDemos[j] = s.tableCreateDemos[j], s.tableCreateDemos[i]
}

// Less is part of sort.Interface. It is implemented by calling the "by" closure in the sorter.
func (s *tableCreateDemoSorter) Less(i, j int) bool {
	return s.by(s.tableCreateDemos[i], s.tableCreateDemos[j])
}

//SelectAll is a auto generated function from SQL query select * from table_create_demo
func (a *TableCreateDemo) SelectAll() ([]*TableCreateDemo, error) {
	querystr := "select * from table_create_demo"
	insArr, err := a.SelectX(querystr)
	if err != nil {
		logger.StackLogger(err)
		return nil, err
	}
	return insArr, err
}

//SelectAkabane is a auto generated function from SQL query select * from table_create_demo where text_demo = '赤羽信之介' or id = 1
func (a *TableCreateDemo) SelectAkabane() (*TableCreateDemo, error) {
	querystr := "select * from table_create_demo where text_demo = '赤羽信之介' or id = 1 "
	insArr, err := a.SelectX(querystr)
	if err != nil {
		logger.StackLogger(err)
		return nil, err
	}

	// Return single part code
	if insArr == nil || len(insArr) == 0 {
		err = errors.New("cannot found the data row")
		logger.StackLogger(err)
		return nil, err
	}
	if len(insArr) > 1 {
		err = errors.New("more than one data row in the search quiteria")
		logger.StackLogger(err)
		return nil, err
	}
	return insArr[0], err
}

//SelectByNameOrIDWithBoolFalse is a auto generated function from SQL query select * from table_create_demo where text_demo = %v or id = %v or bool_demo = false
func (a *TableCreateDemo) SelectByNameOrIDWithBoolFalse(textDemo *string, iD *int) (*TableCreateDemo, error) {
	querystr := "select * from table_create_demo where text_demo = %v or id = %v or bool_demo = false"
	quiteriaArray := []string{}
	quiteriaArray = append(quiteriaArray, "bool_demo = false")
	if textDemo != nil {
		quiteriaArray = append(quiteriaArray, fmt.Sprintf("text_demo = %v", textDemo))
	}
	if iD != nil {
		quiteriaArray = append(quiteriaArray, fmt.Sprintf("id = %v", iD))
	}
	if len(quiteriaArray) != 0 {
		querystr = querystr + " WHERE " + strings.Join(quiteriaArray, " or ")
	}
	insArr, err := a.SelectX(querystr)
	if err != nil {
		logger.StackLogger(err)
		return nil, err
	}

	// Return single part code
	if insArr == nil || len(insArr) == 0 {
		err = errors.New("cannot found the data row")
		logger.StackLogger(err)
		return nil, err
	}
	if len(insArr) > 1 {
		err = errors.New("more than one data row in the search quiteria")
		logger.StackLogger(err)
		return nil, err
	}
	return insArr[0], err
}

//SelectAllTiny is a auto generated function from SQL query select id, int_demo, text_demo from table_create_demo
func (a *TableCreateDemo) SelectAllTiny(tx *sql.Tx) ([]*TableCreateDemo, error) {
	var insArr []*TableCreateDemo
	var rows *sql.Rows
	var err error
	querystr := "select id, int_demo, text_demo from table_create_demo"
	if tx != nil {
		rows, err = tx.Query(querystr)
	} else {
		rows, err = db.Query(querystr)
	}
	if err != nil {
		logger.StackLogger(err)
		return nil, err
	}
	if rows != nil {
		defer rows.Close()
		for rows.Next() {
			item := TableCreateDemo{}
			// replacable
			err := rows.Scan(&item.ID, &item.IntDemo, &item.TextDemo)
			if err != nil {
				logger.StackLogger(err)
				return nil, err
			}
			insArr = append(insArr, &item)
		}
		err = rows.Err()
		if err != nil {
			logger.StackLogger(err)
			return nil, err
		}
	}
	return insArr, err
}

// NewStructSelect is the model for table table_create_demo
type NewStructSelect struct {
	IntDemo  int    `json:"int_demo"`
	TextDemo string `json:"text_demo"`
	TwoInt   int    `json:"two_int"`
	TwoText  string `json:"two_text"`
}

// TestNewStructSelect is a auto generate method for SQL query select int_demo, text_demo, table_create_demo_two.int_demo as two_int, table_create_demo_two.text_demo as two_text from table_create_demo inner join table_create_demo_two on table_create_demo.int_demo = table_create_demo_two.int_demo
func (a *TableCreateDemo) TestNewStructSelect(tx *sql.Tx) ([]*NewStructSelect, error) {
	var insArr []*NewStructSelect
	var rows *sql.Rows
	var err error
	if tx != nil {
		rows, err = tx.Query("select int_demo, text_demo, table_create_demo_two.int_demo as two_int, table_create_demo_two.text_demo as two_text from table_create_demo inner join table_create_demo_two on table_create_demo.int_demo = table_create_demo_two.int_demo")
	} else {
		rows, err = db.Query("select int_demo, text_demo, table_create_demo_two.int_demo as two_int, table_create_demo_two.text_demo as two_text from table_create_demo inner join table_create_demo_two on table_create_demo.int_demo = table_create_demo_two.int_demo")
	}
	if err != nil {
		logger.StackLogger(err)
		return nil, err
	}
	if rows != nil {
		defer rows.Close()
		for rows.Next() {
			item := NewStructSelect{}
			err := rows.Scan(&item.IntDemo, &item.TextDemo, &item.TwoInt, &item.TwoText)
			if err != nil {
				logger.StackLogger(err)
				return nil, err
			}
			insArr = append(insArr, &item)
		}
		err = rows.Err()
		if err != nil {
			logger.StackLogger(err)
			return nil, err
		}
	}
	return insArr, nil
}
